from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Query, Request
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
from data_import_service import (
    analyze_from_url, 
    analyze_from_csv_text, 
    analyze_from_json, 
    create_manual_deal,
    validate_deal_data
)
from mls_service import MLSService
from auth_service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest, CheckoutSessionResponse, CheckoutStatusResponse
from fastapi.responses import StreamingResponse
import io

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

class URLImportRequest(BaseModel):
    url: str
    file_type: str = 'excel'  # excel, csv, json

class CSVImportRequest(BaseModel):
    csv_text: str

class JSONImportRequest(BaseModel):
    json_data: Any

class ManualDealRequest(BaseModel):
    address: str
    price: float
    property_type: Optional[str] = "residential"
    arv: Optional[float] = 0
    estimated_rehab: Optional[float] = 0
    monthly_rent: Optional[float] = 0
    sqft: Optional[float] = 0
    beds: Optional[int] = 0
    baths: Optional[float] = 0
    units: Optional[float] = 1
    occupancy_pct: Optional[float] = 100
    notes: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: str
    user: Dict[str, Any]

# Security
security = HTTPBearer()
auth_service = AuthService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    user = auth_service.verify_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user


# Routes
@api_router.get("/")
async def root():
    return {"message": "DealiQ API - Real Estate Deal Intelligence"}

@api_router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    try:
        user = await auth_service.authenticate_user(request.email, request.password, db)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create JWT token
        token = auth_service.create_token(user)
        
        logger.info(f"User logged in: {user['email']}")
        
        return LoginResponse(
            success=True,
            token=token,
            user=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@api_router.get("/auth/verify")
async def verify_token(user: Dict[str, Any] = Depends(get_current_user)):
    """Verify JWT token and return user data"""
    return {"success": True, "user": user}

class CreateUserRequest(BaseModel):
    email: str
    password: str
    name: str
    plan: str  # Starter, Professional, Enterprise
    state: Optional[str] = None
    mls_access: bool = False

@api_router.post("/admin/users/create")
async def create_user(
    request: CreateUserRequest,
    admin_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new user - Admin only"""
    try:
        # Only admin can create users
        if admin_user.get('id') != 'admin-user':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": request.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Hash password
        password_hash = auth_service.hash_password(request.password)
        
        # Create user document
        user_data = {
            'id': str(uuid.uuid4()),
            'email': request.email,
            'password_hash': password_hash,
            'name': request.name,
            'plan': request.plan,
            'state': request.state or '',
            'mls_access': request.mls_access and request.plan == 'Enterprise',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'active': True
        }
        
        # Insert into database
        await db.users.insert_one(user_data)
        
        logger.info(f"User created: {request.email} - {request.plan} plan")
        
        return {
            "success": True,
            "message": f"User {request.email} created successfully",
            "user": {
                'id': user_data['id'],
                'email': user_data['email'],
                'name': user_data['name'],
                'plan': user_data['plan'],
                'state': user_data['state'],
                'mls_access': user_data['mls_access']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@api_router.get("/admin/users")
async def list_users(admin_user: Dict[str, Any] = Depends(get_current_user)):
    """List all users - Admin only"""
    try:
        # Only admin can list users
        if admin_user.get('id') != 'admin-user':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Get all users from database
        users = await db.users.find({}, {"_id": 0, "password_hash": 0}).to_list(length=None)
        
        return {
            "success": True,
            "count": len(users),
            "users": users
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing users: {str(e)}")

@api_router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: str,
    admin_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a user - Admin only"""
    try:
        # Only admin can delete users
        if admin_user.get('id') != 'admin-user':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Cannot delete admin
        if user_id == 'admin-user':
            raise HTTPException(status_code=400, detail="Cannot delete admin user")
        
        # Delete user
        result = await db.users.delete_one({"id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User deleted: {user_id}")
        
        return {"success": True, "message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

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

@api_router.post("/upload-url", response_model=UploadResponse)
async def upload_from_url(request: URLImportRequest):
    """Import deals from URL (Excel, CSV, or JSON file)"""
    try:
        logger.info(f"Importing deals from URL: {request.url}")
        
        # Validate URL
        if not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL: Must start with http:// or https://")
        
        # Download and analyze
        df = analyze_from_url(request.url, request.file_type)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="No data found in the file")
        
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
            logger.info(f"Stored {len(deals_data)} deals from URL in database")
        
        # Get top deals
        top_deals_data = sorted(deals_data, key=lambda x: x.get('deal_score', 0), reverse=True)[:10]
        top_deals = [Deal(**deal) for deal in top_deals_data]
        
        return UploadResponse(
            success=True,
            message=f"Successfully imported {len(deals_data)} deals from URL",
            deals_count=len(deals_data),
            top_deals=top_deals
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error importing from URL: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error importing from URL: {str(e)}")
        error_msg = str(e)
        
        # Provide helpful error messages
        if "File is not a zip file" in error_msg or "not a valid Excel file" in error_msg:
            error_msg = "The URL does not point to a valid Excel file. Ensure it's a direct download link to an .xlsx or .xls file."
        elif "No such file or directory" in error_msg:
            error_msg = "Failed to download file from URL. Please check the URL is accessible."
        elif "timed out" in error_msg.lower():
            error_msg = "Request timed out. The file might be too large or the server is slow to respond."
        
        raise HTTPException(status_code=500, detail=f"Error importing from URL: {error_msg}")

@api_router.post("/upload-csv", response_model=UploadResponse)
async def upload_from_csv(request: CSVImportRequest):
    """Import deals from CSV text (copy/paste)"""
    try:
        logger.info(f"Importing deals from CSV text")
        
        # Analyze CSV
        df = analyze_from_csv_text(request.csv_text)
        
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
            logger.info(f"Stored {len(deals_data)} deals from CSV in database")
        
        # Get top deals
        top_deals_data = sorted(deals_data, key=lambda x: x.get('deal_score', 0), reverse=True)[:10]
        top_deals = [Deal(**deal) for deal in top_deals_data]
        
        return UploadResponse(
            success=True,
            message=f"Successfully imported {len(deals_data)} deals from CSV",
            deals_count=len(deals_data),
            top_deals=top_deals
        )
        
    except Exception as e:
        logger.error(f"Error importing from CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error importing from CSV: {str(e)}")

@api_router.post("/upload-json", response_model=UploadResponse)
async def upload_from_json(request: JSONImportRequest):
    """Import deals from JSON data"""
    try:
        logger.info(f"Importing deals from JSON")
        
        # Analyze JSON
        df = analyze_from_json(request.json_data)
        
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
            logger.info(f"Stored {len(deals_data)} deals from JSON in database")
        
        # Get top deals
        top_deals_data = sorted(deals_data, key=lambda x: x.get('deal_score', 0), reverse=True)[:10]
        top_deals = [Deal(**deal) for deal in top_deals_data]
        
        return UploadResponse(
            success=True,
            message=f"Successfully imported {len(deals_data)} deals from JSON",
            deals_count=len(deals_data),
            top_deals=top_deals
        )
        
    except Exception as e:
        logger.error(f"Error importing from JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error importing from JSON: {str(e)}")

@api_router.post("/deals/manual", response_model=Deal)
async def create_deal_manually(request: ManualDealRequest):
    """Create a single deal manually"""
    try:
        logger.info(f"Creating manual deal for {request.address}")
        
        # Validate and process
        deal_data = validate_deal_data(request.dict())
        
        # Analyze single deal
        df = create_manual_deal(deal_data)
        
        # Convert to dict
        df['imported_at'] = datetime.now(timezone.utc).isoformat()
        deal = df.to_dict('records')[0]
        
        # Convert numpy types
        for key, value in deal.items():
            if pd.isna(value):
                deal[key] = None
            elif hasattr(value, 'item'):
                deal[key] = value.item()
        
        # Add unique ID
        deal['id'] = str(uuid.uuid4())
        
        # Store in MongoDB
        await db.deals.insert_one(deal)
        logger.info(f"Stored manual deal {deal['id']} in database")
        
        return Deal(**deal)
        
    except Exception as e:
        logger.error(f"Error creating manual deal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating deal: {str(e)}")

# MLS Integration endpoints
class MLSSearchRequest(BaseModel):
    city: Optional[str] = "Las Vegas"
    state: Optional[str] = "NV"
    zipcode: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    beds: Optional[int] = None
    baths: Optional[float] = None
    property_type: Optional[str] = None
    limit: int = 50
    offset: int = 0

class MLSImportRequest(BaseModel):
    property_ids: List[str]

@api_router.post("/mls/search")
async def search_mls_properties(
    request: MLSSearchRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Search MLS properties - Enterprise users with MLS access only"""
    try:
        # Check MLS access
        if not auth_service.has_mls_access(user, request.state):
            raise HTTPException(
                status_code=403,
                detail=f"MLS access not available for your state ({user.get('state', 'N/A')}). Contact support for access."
            )
        # Initialize MLS service
        mls_service = MLSService()
        
        # Search properties
        result = mls_service.search_properties(
            city=request.city,
            state=request.state,
            zipcode=request.zipcode,
            price_min=request.price_min,
            price_max=request.price_max,
            beds=request.beds,
            baths=request.baths,
            property_type=request.property_type,
            limit=request.limit,
            offset=request.offset
        )
        
        logger.info(f"MLS search completed: {result.get('count', 0)} properties found")
        return result
        
    except Exception as e:
        logger.error(f"MLS search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"MLS search error: {str(e)}")

@api_router.get("/mls/property/{mls_id}")
async def get_mls_property(
    mls_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed MLS property information - Enterprise users only"""
    try:
        # Check MLS access
        if not auth_service.has_mls_access(user):
            raise HTTPException(status_code=403, detail="MLS access not available")
        mls_service = MLSService()
        property_data = mls_service.get_property_details(mls_id)
        
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        return property_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching MLS property: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching property: {str(e)}")

@api_router.post("/mls/import", response_model=UploadResponse)
async def import_mls_properties(
    request: MLSImportRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Import selected MLS properties as deals - Enterprise users only"""
    try:
        # Check MLS access
        if not auth_service.has_mls_access(user):
            raise HTTPException(status_code=403, detail="MLS access not available")
        logger.info(f"Importing {len(request.property_ids)} properties from MLS")
        
        # Initialize MLS service
        mls_service = MLSService()
        
        # Get and convert properties
        deals_data = []
        for prop_id in request.property_ids:
            prop_data = mls_service.get_property_details(prop_id)
            if prop_data:
                deal = mls_service.convert_to_deal(prop_data)
                
                # Analyze the deal
                df = create_manual_deal(deal)
                analyzed_deal = df.to_dict('records')[0]
                
                # Convert numpy types
                for key, value in analyzed_deal.items():
                    if pd.isna(value):
                        analyzed_deal[key] = None
                    elif hasattr(value, 'item'):
                        analyzed_deal[key] = value.item()
                
                # Add metadata
                analyzed_deal['id'] = str(uuid.uuid4())
                analyzed_deal['imported_at'] = datetime.now(timezone.utc).isoformat()
                analyzed_deal['import_source'] = 'MLS - Las Vegas GLVAR'
                
                deals_data.append(analyzed_deal)
        
        # Store in MongoDB
        if deals_data:
            await db.deals.insert_many(deals_data)
            logger.info(f"Stored {len(deals_data)} MLS properties in database")
        
        # Get top deals
        top_deals_data = sorted(deals_data, key=lambda x: x.get('deal_score', 0), reverse=True)[:10]
        top_deals = [Deal(**deal) for deal in top_deals_data]
        
        return UploadResponse(
            success=True,
            message=f"Successfully imported {len(deals_data)} properties from MLS",
            deals_count=len(deals_data),
            top_deals=top_deals
        )
        
    except Exception as e:
        logger.error(f"Error importing MLS properties: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error importing properties: {str(e)}")

# Payment endpoints
REPORT_PACKAGES = {
    "premium_report": 25.00  # $25 for comprehensive report with comps
}

@api_router.post("/payments/create-checkout")
async def create_payment_checkout(request: PaymentRequest):
    """Create Stripe checkout session for report purchase"""
    try:
        # Validate deal exists
        deal = await db.deals.find_one({"id": request.deal_id}, {"_id": 0})
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # Get fixed package price (NEVER from frontend)
        amount = REPORT_PACKAGES["premium_report"]
        
        # Initialize Stripe with webhook URL
        stripe_api_key = os.getenv('STRIPE_API_KEY')
        webhook_url = f"{request.origin_url}/api/webhook/stripe"
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url=webhook_url)
        
        # Create success and cancel URLs
        success_url = f"{request.origin_url}/payment-success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{request.origin_url}/deals"
        
        # Create checkout session
        checkout_request = CheckoutSessionRequest(
            amount=float(amount),  # Keep as float
            currency="usd",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "deal_id": request.deal_id,
                "product_type": "premium_report",
                "deal_address": deal.get('address', 'N/A')
            }
        )
        
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record BEFORE redirect
        transaction = {
            "session_id": session.session_id,
            "deal_id": request.deal_id,
            "amount": amount,
            "currency": "usd",
            "payment_status": "pending",
            "status": "initiated",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "metadata": checkout_request.metadata
        }
        
        await db.payment_transactions.insert_one(transaction)
        logger.info(f"Created payment session {session.session_id} for deal {request.deal_id}")
        
        return {"url": session.url, "session_id": session.session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating checkout: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating payment: {str(e)}")

@api_router.get("/payments/status/{session_id}")
async def get_payment_status(session_id: str):
    """Get payment status and update database"""
    try:
        # Initialize Stripe
        stripe_api_key = os.getenv('STRIPE_API_KEY')
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
        
        # Get status from Stripe
        status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Check if already processed to avoid double processing
        transaction = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Only update if status changed and not already marked as paid
        if transaction.get('payment_status') != 'paid' and status.payment_status == 'paid':
            # Update transaction status
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "payment_status": status.payment_status,
                        "status": status.status,
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            logger.info(f"Payment {session_id} marked as paid")
        
        return {
            "session_id": session_id,
            "payment_status": status.payment_status,
            "status": status.status,
            "deal_id": status.metadata.get('deal_id'),
            "can_download": status.payment_status == 'paid'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking payment: {str(e)}")

@api_router.post("/payments/download-report")
async def download_report(request: DownloadRequest):
    """Download report after successful payment"""
    try:
        # Verify payment was completed
        transaction = await db.payment_transactions.find_one(
            {"session_id": request.session_id},
            {"_id": 0}
        )
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        if transaction.get('payment_status') != 'paid':
            raise HTTPException(status_code=403, detail="Payment not completed")
        
        # Get the deal
        deal_id = transaction.get('deal_id')
        deal = await db.deals.find_one({"id": deal_id}, {"_id": 0})
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # Get AI analysis if available
        ai_service = AIAnalysisService()
        try:
            ai_analysis = await ai_service.analyze_deal(deal)
        except:
            ai_analysis = None
        
        # Generate report
        report_service = ReportService()
        excel_bytes = report_service.generate_deal_report(deal, ai_analysis)
        
        # Create filename
        address = deal.get('address', 'deal').replace(' ', '_').replace(',', '')
        filename = f"DealiQ_Report_{address}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        
        logger.info(f"Generated report for deal {deal_id}, session {request.session_id}")
        
        # Return as downloadable file
        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        body = await request.body()
        signature = request.headers.get("Stripe-Signature")
        
        stripe_api_key = os.getenv('STRIPE_API_KEY')
        stripe_checkout = StripeCheckout(api_key=stripe_api_key, webhook_url="")
        
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        # Update transaction if payment succeeded
        if webhook_response.payment_status == 'paid':
            await db.payment_transactions.update_one(
                {"session_id": webhook_response.session_id},
                {
                    "$set": {
                        "payment_status": "paid",
                        "status": "completed",
                        "webhook_received_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            logger.info(f"Webhook processed: Payment {webhook_response.session_id} confirmed")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

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