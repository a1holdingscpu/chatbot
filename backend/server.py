from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import pandas as pd
import tempfile
import shutil
from analyzer_service import analyze_deals_from_excel
from ai_analysis_service import AIAnalysisService
from report_service import ReportService
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest, CheckoutSessionResponse, CheckoutStatusResponse
from fastapi.responses import StreamingResponse

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Define Models
class Deal(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    address: Optional[str] = None
    property_type: Optional[str] = None
    price: float = 0
    deal_score: float = 0
    preferred_strategy: Optional[str] = None
    cap_rate: float = 0
    cash_on_cash_pct: float = 0
    monthly_cashflow: float = 0
    noi: float = 0
    arv: float = 0
    estimated_rehab: float = 0
    arv_spread_pct: float = 0
    wholesale_instant_equity_pct: float = 0
    gross_income_annual: float = 0
    operating_expenses: float = 0
    down_payment_amount: float = 0
    loan_amount: float = 0
    monthly_mortgage: float = 0
    sqft: float = 0
    beds: Optional[int] = None
    baths: Optional[float] = None
    units: float = 0
    occupancy_pct: float = 0
    is_top_deal: bool = False
    imported_at: Optional[str] = None
    
class DealStats(BaseModel):
    total_deals: int
    average_score: float
    top_deals_count: int
    strategy_distribution: Dict[str, int]
    property_type_distribution: Dict[str, int]
    average_cap_rate: float
    average_cash_on_cash: float
    total_value: float

class UploadResponse(BaseModel):
    success: bool
    message: str
    deals_count: int
    top_deals: List[Deal]

class StatusCheckCreate(BaseModel):
    client_name: str

class PaymentRequest(BaseModel):
    deal_id: str
    origin_url: str
    
class DownloadRequest(BaseModel):
    session_id: str


# Routes
@api_router.get("/")
async def root():
    return {"message": "DealIQ Pro API - Real Estate Deal Analyzer"}

@api_router.post("/upload", response_model=UploadResponse)
async def upload_and_analyze(file: UploadFile = File(...)):
    """Upload Excel file and analyze real estate deals"""
    try:
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files are supported")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Analyze deals
        logger.info(f"Analyzing deals from {file.filename}")
        df = analyze_deals_from_excel(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Convert DataFrame to dict records
        df['imported_at'] = datetime.now(timezone.utc).isoformat()
        deals_data = df.to_dict('records')
        
        # Convert numpy types to Python types
        for deal in deals_data:
            for key, value in deal.items():
                if pd.isna(value):
                    deal[key] = None
                elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                    deal[key] = str(value)
                elif hasattr(value, 'item'):  # numpy types
                    deal[key] = value.item()
        
        # Add unique IDs
        for deal in deals_data:
            deal['id'] = str(uuid.uuid4())
        
        # Store in MongoDB
        if deals_data:
            await db.deals.insert_many(deals_data)
            logger.info(f"Stored {len(deals_data)} deals in database")
        
        # Get top deals
        top_deals_data = sorted(deals_data, key=lambda x: x.get('deal_score', 0), reverse=True)[:10]
        top_deals = [Deal(**deal) for deal in top_deals_data]
        
        return UploadResponse(
            success=True,
            message=f"Successfully analyzed {len(deals_data)} deals",
            deals_count=len(deals_data),
            top_deals=top_deals
        )
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing deals: {str(e)}")

@api_router.get("/deals", response_model=List[Deal])
async def get_deals(
    strategy: Optional[str] = Query(None, description="Filter by strategy"),
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    min_score: Optional[float] = Query(None, description="Minimum deal score"),
    limit: int = Query(100, description="Maximum number of results")
):
    """Get all deals with optional filters"""
    try:
        # Build query
        query = {}
        if strategy:
            query['preferred_strategy'] = strategy
        if property_type:
            query['property_type'] = property_type
        if min_score is not None:
            query['deal_score'] = {"$gte": min_score}
        
        # Fetch deals
        deals = await db.deals.find(query, {"_id": 0}).sort("deal_score", -1).limit(limit).to_list(limit)
        
        return [Deal(**deal) for deal in deals]
        
    except Exception as e:
        logger.error(f"Error fetching deals: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching deals: {str(e)}")

@api_router.get("/deals/{deal_id}", response_model=Deal)
async def get_deal(deal_id: str):
    """Get a single deal by ID"""
    try:
        deal = await db.deals.find_one({"id": deal_id}, {"_id": 0})
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        return Deal(**deal)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching deal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching deal: {str(e)}")

@api_router.get("/stats", response_model=DealStats)
async def get_stats():
    """Get analytics and statistics"""
    try:
        deals = await db.deals.find({}, {"_id": 0}).to_list(10000)
        
        if not deals:
            return DealStats(
                total_deals=0,
                average_score=0,
                top_deals_count=0,
                strategy_distribution={},
                property_type_distribution={},
                average_cap_rate=0,
                average_cash_on_cash=0,
                total_value=0
            )
        
        df = pd.DataFrame(deals)
        
        # Calculate statistics
        strategy_dist = df['preferred_strategy'].value_counts().to_dict() if 'preferred_strategy' in df else {}
        property_type_dist = df['property_type'].value_counts().to_dict() if 'property_type' in df else {}
        
        return DealStats(
            total_deals=len(deals),
            average_score=float(df['deal_score'].mean()) if 'deal_score' in df else 0,
            top_deals_count=int(df['is_top_deal'].sum()) if 'is_top_deal' in df else 0,
            strategy_distribution=strategy_dist,
            property_type_distribution=property_type_dist,
            average_cap_rate=float(df['cap_rate'].mean()) if 'cap_rate' in df else 0,
            average_cash_on_cash=float(df['cash_on_cash_pct'].mean()) if 'cash_on_cash_pct' in df else 0,
            total_value=float(df['price'].sum()) if 'price' in df else 0
        )
        
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating stats: {str(e)}")

@api_router.delete("/deals")
async def clear_deals():
    """Clear all deals from database"""
    try:
        result = await db.deals.delete_many({})
        return {"success": True, "deleted_count": result.deleted_count}
    except Exception as e:
        logger.error(f"Error clearing deals: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing deals: {str(e)}")

@api_router.post("/deals/{deal_id}/ai-analysis")
async def get_ai_analysis(deal_id: str):
    """Get AI-powered predictive analysis for a specific deal"""
    try:
        # Get the deal from database
        deal = await db.deals.find_one({"id": deal_id}, {"_id": 0})
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # Initialize AI service
        ai_service = AIAnalysisService()
        
        # Get AI analysis
        analysis = await ai_service.analyze_deal(deal)
        
        logger.info(f"AI analysis completed for deal {deal_id}")
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating AI analysis: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()