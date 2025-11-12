import pandas as pd, os
from pathlib import Path
from analyzer_core import compute_base_metrics, score_deal
proj = Path(__file__).resolve().parents[1]
data_dir = proj / "data"
xlsx = data_dir / "Real_Estate_Deal_Analysis_Toolkit.xlsx"
out_csv = data_dir / "analyzed_deals.csv"
out_summary = data_dir / "ai_summary.txt"
if not xlsx.exists():
    raise FileNotFoundError(f"Input file not found: {xlsx}")
df = pd.read_excel(xlsx, sheet_name=0)
df.columns = [c.strip().lower().replace(" ","_").replace("-","_") for c in df.columns]
# map common names
col_map = {"price_usd":"price","list_price":"price","monthly_rent_usd":"monthly_rent","arv_usd":"arv","rehab_est":"estimated_rehab","beds":"beds","baths":"baths","sq_ft":"sqft"}
for k,v in col_map.items():
    if k in df.columns and v not in df.columns:
        df[v] = df[k]
# create gross_income_annual if monthly_rent
if "monthly_rent" in df.columns and "gross_income_annual" not in df.columns:
    df["monthly_rent"] = pd.to_numeric(df["monthly_rent"], errors="coerce").fillna(0)
    df["gross_income_annual"] = df["monthly_rent"] * 12 * df.get("units",1)
for c in ["price","arv","estimated_rehab","gross_income_annual","sqft","lot_size_acres","units","pads","occupancy_pct"]:
    if c not in df.columns: df[c]=0
df = compute_base_metrics(df)
def suggest_strategy(r):
    if r.get("wholesale_instant_equity_pct",0) >= 20 and r.get("assignment_allowed",False):
        return "wholesale"
    if r.get("arv_spread_pct",0) >= 25 and r.get("estimated_rehab",0) <= r.get("price",0)*0.3:
        return "flip"
    if r.get("cap_rate",0) >= 8 and r.get("cash_on_cash_pct",0) >= 10:
        return "buy_hold"
    if r.get("subject_to_possible",False):
        return "subject_to"
    if r.get("seller_finance_available",False):
        return "seller_finance"
    return "hold"
df["deal_score"] = df.apply(lambda r: score_deal(r), axis=1)
df["preferred_strategy"] = df.apply(suggest_strategy, axis=1)
df["is_top_deal"] = df["deal_score"] >= int(os.getenv("MIN_DEAL_SCORE","70"))
df["imported_at"] = pd.Timestamp.now()
df.to_csv(out_csv, index=False)
topn = df.sort_values("deal_score", ascending=False).head(10)
lines = ["DealIQ Pro - Top Deals Summary","=============================="]
for i, row in topn.iterrows():
    lines.append(f"{int(row.deal_score)} | {row.get('address','(no address)')} | ${row.get('price',0):,.0f} | Strategy: {row.get('preferred_strategy')} | CapRate: {row.get('cap_rate'):.2f}%")
lines.append("")    
lines.append("Brief insights:")
avg_score = df['deal_score'].mean() if len(df)>0 else 0
lines.append(f"Average deal score: {avg_score:.1f}")
parks = df[df['property_type'].str.contains('park', na=False, case=False)] if 'property_type' in df.columns else df[[]]
try:
    if 'deal_score' in parks.columns and len(parks)>0:
        ptop = parks.sort_values('deal_score', ascending=False).iloc[0]
        pads = ptop.get('pads', ptop.get('units',1)) or 1
        lines.append(f"Top park: {ptop.get('address','(no address)')} — NOI per pad: {int(ptop.get('noi',0)/pads) if pads>0 else 0}")
except Exception:
    pass
with open(out_summary,'w',encoding='utf8') as f:
    f.write('\n'.join(lines))
print('Processed', len(df), 'rows. CSV:', out_csv, 'Summary:', out_summary)
print(topn[[c for c in topn.columns if c in ['address','price','deal_score','preferred_strategy','cap_rate']]].head(10))
