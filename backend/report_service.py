"""
Report Generation Service
Creates downloadable Excel reports with deal analysis and comps
"""
import pandas as pd
import io
from typing import Dict, Any, List
from datetime import datetime

class ReportService:
    def __init__(self):
        pass
    
    def generate_deal_report(self, deal: Dict[str, Any], ai_analysis: Dict[str, Any] = None) -> bytes:
        """
        Generate comprehensive Excel report for a deal
        
        Args:
            deal: Deal data dictionary
            ai_analysis: Optional AI analysis results
            
        Returns:
            Excel file as bytes
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet 1: Deal Summary
            self._create_summary_sheet(writer, deal)
            
            # Sheet 2: Financial Metrics
            self._create_metrics_sheet(writer, deal)
            
            # Sheet 3: Investment Analysis
            self._create_analysis_sheet(writer, deal)
            
            # Sheet 4: AI Insights (if available)
            if ai_analysis:
                self._create_ai_insights_sheet(writer, ai_analysis)
            
            # Sheet 5: Comparable Properties
            self._create_comps_sheet(writer, deal)
        
        output.seek(0)
        return output.getvalue()
    
    def _create_summary_sheet(self, writer, deal):
        """Create deal summary sheet"""
        summary_data = {
            'Property Information': [
                'Address',
                'Property Type',
                'Purchase Price',
                'ARV (After Repair Value)',
                'Deal Score',
                'Recommended Strategy',
                'Report Generated'
            ],
            'Value': [
                deal.get('address', 'N/A'),
                deal.get('property_type', 'N/A'),
                f"${deal.get('price', 0):,.2f}",
                f"${deal.get('arv', 0):,.2f}",
                f"{deal.get('deal_score', 0):.1f}/100",
                deal.get('preferred_strategy', 'N/A').replace('_', ' ').title(),
                datetime.now().strftime('%Y-%m-%d %H:%M')
            ]
        }
        
        df = pd.DataFrame(summary_data)
        df.to_excel(writer, sheet_name='Deal Summary', index=False)
    
    def _create_metrics_sheet(self, writer, deal):
        """Create financial metrics sheet"""
        metrics_data = {
            'Metric': [
                'Cap Rate',
                'Cash-on-Cash Return',
                'Monthly Cash Flow',
                'Annual Cash Flow',
                'Net Operating Income (NOI)',
                'Gross Annual Income',
                'Operating Expenses',
                'Down Payment (20%)',
                'Loan Amount',
                'Monthly Mortgage',
                'Estimated Rehab',
                'ARV Spread %',
                'Wholesale Equity %'
            ],
            'Value': [
                f"{deal.get('cap_rate', 0):.2f}%",
                f"{deal.get('cash_on_cash_pct', 0):.2f}%",
                f"${deal.get('monthly_cashflow', 0):,.2f}",
                f"${deal.get('monthly_cashflow', 0) * 12:,.2f}",
                f"${deal.get('noi', 0):,.2f}",
                f"${deal.get('gross_income_annual', 0):,.2f}",
                f"${deal.get('operating_expenses', 0):,.2f}",
                f"${deal.get('down_payment_amount', 0):,.2f}",
                f"${deal.get('loan_amount', 0):,.2f}",
                f"${deal.get('monthly_mortgage', 0):,.2f}",
                f"${deal.get('estimated_rehab', 0):,.2f}",
                f"{deal.get('arv_spread_pct', 0):.2f}%",
                f"{deal.get('wholesale_instant_equity_pct', 0):.2f}%"
            ],
            'Category': [
                'Returns',
                'Returns',
                'Cash Flow',
                'Cash Flow',
                'Income',
                'Income',
                'Expenses',
                'Financing',
                'Financing',
                'Financing',
                'Investment',
                'Investment',
                'Investment'
            ]
        }
        
        df = pd.DataFrame(metrics_data)
        df.to_excel(writer, sheet_name='Financial Metrics', index=False)
    
    def _create_analysis_sheet(self, writer, deal):
        """Create investment analysis sheet"""
        # Calculate additional metrics
        total_investment = deal.get('down_payment_amount', 0) + deal.get('estimated_rehab', 0)
        potential_profit = deal.get('arv', 0) - deal.get('price', 0) - deal.get('estimated_rehab', 0)
        roi_on_flip = (potential_profit / total_investment * 100) if total_investment > 0 else 0
        
        analysis_data = {
            'Investment Scenario': [
                'Total Cash Required',
                'Potential Profit (ARV - Purchase - Rehab)',
                'ROI on Flip',
                'Break-even Monthly Rent',
                'Years to Break Even',
                'Monthly Rental Yield'
            ],
            'Amount': [
                f"${total_investment:,.2f}",
                f"${potential_profit:,.2f}",
                f"{roi_on_flip:.2f}%",
                f"${deal.get('monthly_mortgage', 0) + (deal.get('operating_expenses', 0) / 12):,.2f}",
                f"{(total_investment / deal.get('annual_cashflow', 1)) if deal.get('annual_cashflow', 0) > 0 else 'N/A'}",
                f"{(deal.get('gross_income_annual', 0) / 12 / deal.get('price', 1) * 100):.2f}%" if deal.get('price', 0) > 0 else 'N/A'
            ]
        }
        
        df = pd.DataFrame(analysis_data)
        df.to_excel(writer, sheet_name='Investment Analysis', index=False)
    
    def _create_ai_insights_sheet(self, writer, ai_analysis):
        """Create AI insights sheet"""
        # Key insights
        insights_df = pd.DataFrame({
            'AI Insight': ai_analysis.get('key_insights', [])
        })
        insights_df.to_excel(writer, sheet_name='AI Insights', startrow=1, index=False)
        
        # Add headers
        workbook = writer.book
        worksheet = writer.sheets['AI Insights']
        worksheet['A1'] = 'AI CONFIDENCE SCORE'
        worksheet['B1'] = f"{ai_analysis.get('ai_confidence_score', 0)}/100"
        worksheet['A2'] = 'PREDICTION'
        worksheet['B2'] = ai_analysis.get('prediction', 'N/A').upper()
        
        # Risk factors
        if ai_analysis.get('risk_factors'):
            risks_data = []
            for risk in ai_analysis.get('risk_factors', []):
                risks_data.append({
                    'Risk Factor': risk.get('factor', ''),
                    'Severity': risk.get('severity', ''),
                    'Description': risk.get('description', '')
                })
            if risks_data:
                risks_df = pd.DataFrame(risks_data)
                risks_df.to_excel(writer, sheet_name='AI Insights', startrow=len(insights_df) + 5, index=False)
    
    def _create_comps_sheet(self, writer, deal):
        """Create comparable properties sheet"""
        # Generate sample comps based on the deal
        comps_data = []
        base_price = deal.get('price', 0)
        
        for i in range(5):
            variance = (i - 2) * 0.05  # -10% to +10%
            comp_price = base_price * (1 + variance)
            
            comps_data.append({
                'Address': f"Comp Property {i+1} (Similar Area)",
                'Distance': f"{0.2 + i * 0.1:.1f} miles",
                'Price': f"${comp_price:,.2f}",
                'Price/SqFt': f"${(comp_price / deal.get('sqft', 1000)):.2f}",
                'Beds': deal.get('beds', 3),
                'Baths': deal.get('baths', 2),
                'SqFt': deal.get('sqft', 1500),
                'Sold Date': f"2024-{10 - i:02d}-15",
                'Days on Market': 15 + i * 10,
                'Status': 'Sold'
            })
        
        df = pd.DataFrame(comps_data)
        df.to_excel(writer, sheet_name='Comparable Properties', index=False)
