# DealIQ Pro - Real Estate Deal Analyzer & Investor Portal

## Overview
DealIQ Pro is a complete real estate investment platform combining a **public-facing investor portal** with a powerful **internal deal analysis tool**. 

### Two Integrated Applications:

**1. Investor Landing Page (`/`)** - Public Marketing Site
- Professional investor-focused landing page
- Live animated portfolio metrics dashboard
- Active deal pipeline showcase
- Company track record and performance history
- Investment opportunity presentations
- Call-to-action for investor engagement

**2. Deal Analyzer Tool (`/analyzer/*`)** - Internal Analysis Platform
- Upload Excel files and analyze real estate deals instantly
- Proprietary scoring algorithm (0-100) for different property types
- Complete financial projections and ROI calculations
- Advanced filtering, sorting, and deal comparison
- Portfolio analytics and performance tracking

## Features

### 🎯 Deal Analysis
- **Automated Scoring**: Proprietary algorithm scores deals 0-100 based on property type
- **Strategy Recommendations**: Get optimal investment strategies (Wholesale, Flip, Buy & Hold, etc.)
- **Financial Metrics**: Complete analysis including Cap Rate, Cash-on-Cash returns, NOI, cash flow

### 📊 Analytics Dashboard
- Portfolio overview with key performance metrics
- Strategy and property type distribution charts
- Top performing deals tracking
- Real-time statistics and insights

### 📁 File Upload
- Drag-and-drop Excel file upload
- Instant analysis of multiple deals
- Batch processing of property portfolios

### 🔍 Deal Management
- Searchable and filterable deal table
- Sort by any metric (score, price, cap rate, etc.)
- Detailed view of all financial calculations
- Strategy-based filtering

## Tech Stack

**Frontend:**
- React 19
- Tailwind CSS
- Shadcn/UI Components
- React Router
- Axios

**Backend:**
- FastAPI (Python)
- MongoDB (Motor async driver)
- Pandas & NumPy for analytics
- OpenPyXL for Excel processing

## API Endpoints

```
GET  /api/              - Health check
POST /api/upload        - Upload and analyze Excel file
GET  /api/deals         - Get all deals (with filters)
GET  /api/deals/{id}    - Get single deal details
GET  /api/stats         - Get portfolio analytics
DELETE /api/deals       - Clear all deals
```

## Excel File Format

Your Excel file should include columns such as:
- `address` - Property address
- `property_type` - Type (residential, commercial, land, rv_park, mobile_home_park)
- `price` - Purchase price
- `monthly_rent` - Monthly rental income
- `arv` - After Repair Value
- `estimated_rehab` - Rehab costs
- `beds`, `baths`, `sqft` - Property details
- `taxes`, `insurance` - Annual costs

## Deal Scoring

DealIQ Pro uses different scoring algorithms based on property type:

**Residential** (0-100):
- Cap Rate (30 points)
- Cash-on-Cash Return (25 points)
- ARV Spread (20 points)
- Wholesale Equity (10 points)
- Days on Market (5 points)

**Commercial** (0-100):
- Cap Rate (30 points)
- NOI Percentage (25 points)
- Occupancy (20 points)
- Capital Expenditure (15 points)
- ARV Spread (10 points)

**Land** (0-100):
- ARV Spread (40 points)
- Lot Size (20 points)
- Zoning (20 points)
- Wholesale Equity (20 points)

**Mobile Home/RV Parks** (0-100):
- Occupancy (30 points)
- NOI per Pad (25 points)
- Capital Expenditure (20 points)
- ARV Spread (15 points)
- Management Efficiency (10 points)

## Investment Strategies

1. **Wholesale**: High equity deals (20%+) with assignment rights
2. **Flip**: Strong ARV spread (25%+) with manageable rehab
3. **Buy & Hold**: High cap rate (8%+) and cash flow (10%+ CoC)
4. **Subject To**: Properties with subject-to financing available
5. **Seller Finance**: Owner-financed opportunities
6. **Hold**: Properties worth monitoring for future potential

## Getting Started

1. **Upload Deals**: Navigate to Upload page and drop your Excel file
2. **View Analysis**: Check Dashboard for portfolio overview
3. **Browse Deals**: Visit Deals page to filter and sort opportunities
4. **Deep Dive**: Click any deal to view complete financial breakdown
5. **Track Performance**: Use Analytics to monitor portfolio metrics

## Sample Data

A sample Excel file with realistic deal data is included at:
`/app/data/sample_deals.xlsx`

## Development

**Start Services:**
```bash
sudo supervisorctl start all
```

**Backend:**
```bash
cd /app/backend
pip install -r requirements.txt
uvicorn server:app --reload
```

**Frontend:**
```bash
cd /app/frontend
yarn install
yarn start
```

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│   React     │────────▶│   FastAPI    │────────▶│   MongoDB    │
│  Frontend   │  HTTP   │   Backend    │  Motor  │   Database   │
└─────────────┘         └──────────────┘         └──────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │   Analyzer   │
                        │   Service    │
                        └──────────────┘
```

## License

Proprietary - DealIQ Pro

## Support

For questions or issues, please refer to the documentation or contact support.
