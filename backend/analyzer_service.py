"""
Real Estate Deal Analyzer Service
Integrates the analyzer_core logic for deal analysis
"""
import math
import numpy as np
import pandas as pd
from typing import Dict, Any

DEFAULTS = {
    "DOWN_PAYMENT_PCT": 0.20,
    "INTEREST_RATE": 7.0,
    "LOAN_YEARS": 30,
    "VACANCY": 0.05,
    "MAINTENANCE_PCT": 0.10,
    "MGMT_PCT": 0.08
}

def monthly_mortgage(loan, annual_rate=DEFAULTS["INTEREST_RATE"], years=DEFAULTS["LOAN_YEARS"]):
    """Calculate monthly mortgage payment"""
    if loan <= 0 or annual_rate <= 0:
        return 0.0
    r = annual_rate / 100 / 12
    n = years * 12
    return loan * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def compute_base_metrics(df):
    """Compute all financial metrics for deals"""
    # Ensure required columns exist
    for c in ["price", "gross_income_annual", "estimated_rehab", "sqft", 
              "lot_size_acres", "units", "pads", "occupancy_pct"]:
        if c not in df.columns:
            df[c] = 0
    
    # Convert to numeric
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["gross_income_annual"] = pd.to_numeric(df["gross_income_annual"], errors="coerce").fillna(0)
    df["estimated_rehab"] = pd.to_numeric(df["estimated_rehab"], errors="coerce").fillna(0)
    df["sqft"] = pd.to_numeric(df["sqft"], errors="coerce").fillna(0)
    df["lot_size_acres"] = pd.to_numeric(df["lot_size_acres"], errors="coerce").fillna(0)
    df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0)
    df["pads"] = pd.to_numeric(df["pads"], errors="coerce").fillna(df["units"])
    df["occupancy_pct"] = pd.to_numeric(df["occupancy_pct"], errors="coerce").fillna(0)
    
    # Calculate financing
    df["down_payment_amount"] = df["price"] * DEFAULTS["DOWN_PAYMENT_PCT"]
    df["loan_amount"] = df["price"] - df["down_payment_amount"]
    df["monthly_mortgage"] = df["loan_amount"].apply(lambda x: monthly_mortgage(x))
    
    # Calculate expenses
    df["vacancy_loss"] = df["gross_income_annual"] * df.get("vacancy_pct", DEFAULTS["VACANCY"])
    df["maintenance"] = df["gross_income_annual"] * df.get("maintenance_pct", DEFAULTS["MAINTENANCE_PCT"])
    df["management"] = df["gross_income_annual"] * df.get("management_pct", DEFAULTS["MGMT_PCT"])
    df["hoa"] = df.get("hoa", 0)
    df["operating_expenses"] = (
        df.get("taxes", 0) + 
        df.get("insurance", 0) + 
        df["maintenance"] + 
        df["management"] + 
        df.get("hoa", 0) + 
        df.get("utilities_expenses", 0)
    )
    
    # Calculate returns
    df["noi"] = df["gross_income_annual"] - df["vacancy_loss"] - df["operating_expenses"]
    df["cap_rate"] = np.where(df["price"] > 0, df["noi"] / df["price"] * 100, 0)
    df["monthly_cashflow"] = df["noi"] / 12 - df["monthly_mortgage"]
    df["annual_cashflow"] = df["monthly_cashflow"] * 12
    df["cash_on_cash_pct"] = np.where(
        df["down_payment_amount"] > 0, 
        df["annual_cashflow"] / df["down_payment_amount"] * 100, 
        0
    )
    
    # Calculate ARV metrics
    df["arv_spread_pct"] = np.where(
        df["price"] > 0, 
        (df.get("arv", 0) - df["price"] - df.get("estimated_rehab", 0)) / df["price"] * 100, 
        0
    )
    df["estimated_flip_profit"] = (
        df.get("arv", 0) - 
        (df["price"] + df.get("estimated_rehab", 0) + (df.get("arv", 0) * 0.10))
    )
    df["wholesale_instant_equity_pct"] = np.where(
        df["price"] > 0, 
        (df.get("arv", 0) - df["price"]) / df.get("arv", 1) * 100, 
        0
    )
    
    return df

def score_residential(r):
    """Score residential properties"""
    score = 0.0
    score += min(max(r.get("cap_rate", 0), 0), 15) / 15 * 30
    score += min(max(r.get("cash_on_cash_pct", 0), 0), 30) / 30 * 25
    arv = min(max(r.get("arv_spread_pct", -50), -50), 50)
    score += ((arv + 50) / 100.0) * 20.0
    score += min(max(r.get("wholesale_instant_equity_pct", 0), 0), 50) / 50 * 10
    dom = r.get("days_on_market")
    score += 5 if dom is None else max(0, (1 - min(dom, 180) / 180) * 5)
    return round(score, 1)

def score_commercial(r):
    """Score commercial properties"""
    score = 0.0
    score += min(max(r.get("cap_rate", 0), 0), 12) / 12 * 30
    noi_pct = min(max(r.get("noi", 0) / max(r.get("price", 1), 1) * 100, 0), 20)
    score += noi_pct / 20 * 25
    occ = r.get("occupancy_pct", 75)
    score += min(max(occ, 0), 100) / 100 * 20
    capex = r.get("capex_needed", 0)
    score += (1 - min(capex / max(r.get("price", 1), 1), 1)) * 15
    score += min(max(r.get("arv_spread_pct", 0), 0), 50) / 50 * 10
    return round(score, 1)

def score_land(r):
    """Score land properties"""
    score = 0.0
    score += min(max(r.get("arv_spread_pct", 0), 0), 100) / 100 * 40
    lot = r.get("lot_size_acres", 0)
    score += (1 - math.exp(-lot)) * 20
    if r.get("zoning_notes"):
        score += 20
    else:
        score += 10
    score += min(max(r.get("wholesale_instant_equity_pct", 0), 0), 50) / 50 * 20
    return round(score, 1)

def score_park(r):
    """Score mobile home/RV parks"""
    score = 0.0
    occ = r.get("occupancy_pct", 70)
    score += min(max(occ, 0), 100) / 100 * 30
    pads = max(r.get("pads", r.get("units", 0)), 1)
    noi_per_pad = 0 if pads == 0 else r.get("noi", 0) / pads
    score += min(max(noi_per_pad / 2000, 0), 5) / 5 * 25
    capex = r.get("capex_needed", 0)
    score += (1 - min(capex / max(r.get("price", 1), 1), 1)) * 20
    score += min(max(r.get("arv_spread_pct", 0), 0), 50) / 50 * 15
    mgmt = r.get("management_pct", DEFAULTS["MGMT_PCT"])
    score += (1 - min(mgmt, 0.5) / 0.5) * 10
    return round(score, 1)

def score_deal(row):
    """Score a deal based on property type"""
    t = (row.get("property_type") or "").lower()
    if t in ["rv_park", "mobile_home_park"]:
        return score_park(row)
    elif t in ["land"]:
        return score_land(row)
    elif t in ["commercial", "retail", "office", "industrial"]:
        return score_commercial(row)
    else:
        return score_residential(row)

def suggest_strategy(r):
    """Suggest best investment strategy"""
    if r.get("wholesale_instant_equity_pct", 0) >= 20 and r.get("assignment_allowed", False):
        return "wholesale"
    if r.get("arv_spread_pct", 0) >= 25 and r.get("estimated_rehab", 0) <= r.get("price", 0) * 0.3:
        return "flip"
    if r.get("cap_rate", 0) >= 8 and r.get("cash_on_cash_pct", 0) >= 10:
        return "buy_hold"
    if r.get("subject_to_possible", False):
        return "subject_to"
    if r.get("seller_finance_available", False):
        return "seller_finance"
    return "hold"

def analyze_deals_from_excel(file_path: str) -> pd.DataFrame:
    """
    Analyze real estate deals from Excel file
    Returns DataFrame with all computed metrics
    """
    # Read Excel file
    df = pd.read_excel(file_path, sheet_name=0)
    
    # Clean column names
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    
    # Map common column names
    col_map = {
        "price_usd": "price",
        "list_price": "price",
        "monthly_rent_usd": "monthly_rent",
        "arv_usd": "arv",
        "rehab_est": "estimated_rehab",
        "beds": "beds",
        "baths": "baths",
        "sq_ft": "sqft"
    }
    
    for k, v in col_map.items():
        if k in df.columns and v not in df.columns:
            df[v] = df[k]
    
    # Create gross_income_annual if monthly_rent exists
    if "monthly_rent" in df.columns and "gross_income_annual" not in df.columns:
        df["monthly_rent"] = pd.to_numeric(df["monthly_rent"], errors="coerce").fillna(0)
        df["gross_income_annual"] = df["monthly_rent"] * 12 * df.get("units", 1)
    
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
