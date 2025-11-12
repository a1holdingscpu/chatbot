"""
Data Import Service
Handles various import methods: URL, CSV, JSON, manual entry
"""
import pandas as pd
import requests
import tempfile
import os
import json
from typing import Dict, Any, List
from analyzer_service import analyze_deals_from_excel, compute_base_metrics, score_deal, suggest_strategy

def download_file_from_url(url: str) -> str:
    """Download file from URL and return temp file path"""
    response = requests.get(url, timeout=30, stream=True)
    response.raise_for_status()
    
    # Get file extension from URL or content-type
    content_type = response.headers.get('content-type', '')
    if 'spreadsheet' in content_type or url.endswith('.xlsx'):
        ext = '.xlsx'
    elif url.endswith('.xls'):
        ext = '.xls'
    elif 'csv' in content_type or url.endswith('.csv'):
        ext = '.csv'
    elif 'json' in content_type or url.endswith('.json'):
        ext = '.json'
    else:
        ext = '.xlsx'  # default
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        for chunk in response.iter_content(chunk_size=8192):
            tmp_file.write(chunk)
        return tmp_file.name

def analyze_from_url(url: str, file_type: str = 'excel') -> pd.DataFrame:
    """
    Download and analyze deals from URL
    Supports Excel, CSV, and JSON formats
    """
    temp_path = download_file_from_url(url)
    
    try:
        if file_type == 'excel' or temp_path.endswith(('.xlsx', '.xls')):
            df = analyze_deals_from_excel(temp_path)
        elif file_type == 'csv' or temp_path.endswith('.csv'):
            df = analyze_from_csv_file(temp_path)
        elif file_type == 'json' or temp_path.endswith('.json'):
            with open(temp_path, 'r') as f:
                data = json.load(f)
            df = analyze_from_json(data)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return df
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def analyze_from_csv_file(file_path: str) -> pd.DataFrame:
    """Analyze deals from CSV file"""
    df = pd.read_csv(file_path)
    return process_dataframe(df)

def analyze_from_csv_text(csv_text: str) -> pd.DataFrame:
    """Analyze deals from CSV text (copy/paste)"""
    from io import StringIO
    df = pd.read_csv(StringIO(csv_text))
    return process_dataframe(df)

def analyze_from_json(data: Any) -> pd.DataFrame:
    """Analyze deals from JSON data"""
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # Handle nested structures
        if 'deals' in data:
            df = pd.DataFrame(data['deals'])
        elif 'data' in data:
            df = pd.DataFrame(data['data'])
        elif 'properties' in data:
            df = pd.DataFrame(data['properties'])
        else:
            # Single deal
            df = pd.DataFrame([data])
    else:
        raise ValueError("JSON must be array or object with deals/data/properties key")
    
    return process_dataframe(df)

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process any dataframe and apply deal analysis logic
    Similar to analyze_deals_from_excel but more flexible
    """
    # Clean column names
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    
    # Map common column names
    col_map = {
        "price_usd": "price",
        "list_price": "price",
        "asking_price": "price",
        "purchase_price": "price",
        "monthly_rent_usd": "monthly_rent",
        "monthly_income": "monthly_rent",
        "arv_usd": "arv",
        "after_repair_value": "arv",
        "rehab_est": "estimated_rehab",
        "rehab_cost": "estimated_rehab",
        "repair_costs": "estimated_rehab",
        "bedrooms": "beds",
        "bed": "beds",
        "bathrooms": "baths",
        "bath": "baths",
        "sq_ft": "sqft",
        "square_feet": "sqft",
        "sqft.": "sqft",
        "property_address": "address",
        "street_address": "address",
        "type": "property_type",
        "prop_type": "property_type"
    }
    
    for k, v in col_map.items():
        if k in df.columns and v not in df.columns:
            df[v] = df[k]
    
    # Create gross_income_annual if monthly_rent exists
    if "monthly_rent" in df.columns and "gross_income_annual" not in df.columns:
        df["monthly_rent"] = pd.to_numeric(df["monthly_rent"], errors="coerce").fillna(0)
        units = df.get("units", 1)
        df["gross_income_annual"] = df["monthly_rent"] * 12 * units
    
    # Ensure required columns
    for c in ["price", "arv", "estimated_rehab", "gross_income_annual", "sqft", 
              "lot_size_acres", "units", "pads", "occupancy_pct"]:
        if c not in df.columns:
            df[c] = 0
    
    # Compute metrics
    df = compute_base_metrics(df)
    
    # Score and strategy
    df["deal_score"] = df.apply(lambda r: score_deal(r), axis=1)
    df["preferred_strategy"] = df.apply(suggest_strategy, axis=1)
    df["is_top_deal"] = df["deal_score"] >= 70
    
    return df

def create_manual_deal(deal_data: Dict[str, Any]) -> pd.DataFrame:
    """Create a single deal from manual entry"""
    # Convert to DataFrame with one row
    df = pd.DataFrame([deal_data])
    return process_dataframe(df)

def validate_deal_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean deal data"""
    required_fields = ['address', 'price']
    
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")
    
    # Convert numeric fields
    numeric_fields = ['price', 'arv', 'estimated_rehab', 'monthly_rent', 'sqft', 
                     'beds', 'baths', 'units', 'occupancy_pct']
    
    for field in numeric_fields:
        if field in data and data[field]:
            try:
                data[field] = float(data[field])
            except (ValueError, TypeError):
                data[field] = 0
    
    return data
