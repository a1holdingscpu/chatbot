# DealiQ Pro - Usage Guide

## Quick Start

### 1. Access the Application
Open your browser and navigate to the application URL. You'll see the Dashboard with navigation menu.

### 2. Upload Your First File

**Step 1:** Click on "Upload" in the navigation menu

**Step 2:** Drag and drop your Excel file or click to browse
- Supported formats: `.xlsx`, `.xls`
- The file should contain columns for property details (price, address, rent, etc.)

**Step 3:** Click "Upload & Analyze" button
- The system will process your file
- Analysis typically takes 2-5 seconds
- You'll see a success message with preview of top deals

**Step 4:** View results by clicking:
- "View All Deals" - See complete list
- "View Analytics" - See portfolio statistics

### 3. Browse and Filter Deals

**Navigate to Deals page:**
- Use the search box to find specific addresses
- Filter by investment strategy (Wholesale, Flip, Buy & Hold, etc.)
- Sort by any metric (Score, Price, Cap Rate, Cash Flow)
- Toggle between ascending/descending order

**View Deal Details:**
- Click the eye icon (👁) on any deal row
- See complete financial breakdown including:
  - Purchase details and financing
  - Return metrics (Cap Rate, CoC, Cash Flow, NOI)
  - Income and expenses
  - Property specifications

### 4. Analyze Your Portfolio

**Navigate to Analytics page to see:**

**Key Metrics:**
- Total number of deals analyzed
- Average deal score
- Average cap rate and cash-on-cash return
- Total portfolio value

**Distribution Charts:**
- Investment strategy breakdown
- Property type distribution
- Visual representation with percentages

**Top Performers:**
- Ranked list of highest scoring deals
- Quick access to best opportunities

## Understanding Deal Scores

### Score Ranges:
- **70-100**: Excellent deals (highlighted as "top deals")
- **50-69**: Good opportunities worth considering
- **30-49**: Average deals, may have potential
- **0-29**: Below average, proceed with caution

### Scoring Factors:

**For Residential Properties:**
- Cap Rate (30%)
- Cash-on-Cash Return (25%)
- ARV Spread (20%)
- Wholesale Equity (10%)
- Days on Market (5%)

**For Commercial Properties:**
- Cap Rate (30%)
- NOI Percentage (25%)
- Occupancy Rate (20%)
- Capital Expenditure (15%)
- ARV Spread (10%)

## Investment Strategies Explained

### 1. Wholesale
**When Recommended:**
- Property has 20%+ instant equity
- Assignment rights available
- Quick turnaround potential

**Action:** Secure under contract and assign to end buyer

### 2. Flip
**When Recommended:**
- ARV spread is 25%+
- Rehab costs under 30% of purchase price
- Strong resale market

**Action:** Buy, renovate, and sell for profit

### 3. Buy & Hold
**When Recommended:**
- Cap rate 8% or higher
- Cash-on-cash return 10%+
- Strong rental market

**Action:** Purchase and hold for rental income and appreciation

### 4. Subject To
**When Recommended:**
- Property allows subject-to financing
- Current financing is favorable

**Action:** Take over existing mortgage payments

### 5. Seller Finance
**When Recommended:**
- Owner willing to carry financing
- Favorable terms available

**Action:** Negotiate owner financing terms

### 6. Hold
**When Recommended:**
- Deal doesn't meet other criteria yet
- Market conditions may improve

**Action:** Monitor and revisit later

## Key Metrics Explained

### Cap Rate (Capitalization Rate)
- Formula: NOI ÷ Purchase Price × 100
- Measures annual return on investment
- Higher is better (8%+ is excellent)

### Cash-on-Cash Return
- Formula: Annual Cash Flow ÷ Down Payment × 100
- Measures return on actual cash invested
- Target: 10%+ for buy and hold

### NOI (Net Operating Income)
- Formula: Gross Income - Operating Expenses
- Shows property's actual profit potential
- Excludes mortgage payments

### Monthly Cash Flow
- Formula: NOI ÷ 12 - Monthly Mortgage
- Your monthly profit or loss
- Positive cash flow is ideal for rentals

### ARV Spread
- Formula: (ARV - Price - Rehab) ÷ Price × 100
- Shows profit potential after improvements
- 25%+ is excellent for flips

## Tips for Success

### 1. Data Quality
- Ensure accurate property information
- Include all expense categories
- Verify market rents and values
- Update regularly for best results

### 2. Filter Strategies
- Start with deals scoring 70+
- Filter by your preferred strategy
- Sort by cash flow for rentals
- Sort by ARV spread for flips

### 3. Due Diligence
- Use DealiQ scores as a starting point
- Always verify with local market data
- Inspect properties in person
- Consult with local professionals

### 4. Portfolio Management
- Upload new deals regularly
- Track performance over time
- Compare deals side-by-side
- Monitor strategy distribution

## Sample Excel Format

Your Excel file should include these columns (minimum):

**Required:**
- `address` - Property location
- `price` - Purchase price
- `property_type` - residential, commercial, land, etc.

**Recommended:**
- `monthly_rent` - Monthly rental income
- `arv` - After Repair Value
- `estimated_rehab` - Renovation costs
- `beds`, `baths`, `sqft` - Property specs
- `taxes`, `insurance` - Annual costs

**Optional:**
- `units` - Number of units (for multifamily)
- `occupancy_pct` - Current occupancy
- `assignment_allowed` - Boolean
- `seller_finance_available` - Boolean

## Troubleshooting

### File Upload Issues
- **Error: "Only Excel files supported"**
  - Solution: Ensure file has .xlsx or .xls extension

- **Error: "Failed to analyze deals"**
  - Solution: Check that required columns exist (address, price, property_type)

### Missing Data
- **Deals show 0 for all metrics**
  - Solution: Add financial data (monthly_rent, taxes, insurance)

- **All deals score 15**
  - Solution: Ensure property_type column is filled correctly

### Navigation Issues
- **Pages not loading**
  - Solution: Check browser console for errors
  - Refresh the page
  - Clear browser cache

## Support

For additional help:
1. Check the README.md for technical details
2. Review the sample data file at `/app/data/sample_deals.xlsx`
3. Ensure all services are running: `sudo supervisorctl status`

---

**Remember:** DealiQ Pro provides analysis and recommendations, but always conduct your own due diligence before making investment decisions.
