"""
AI-Powered Predictive Deal Analysis Service
Uses LLM to provide intelligent insights on real estate deals
"""
import os
import json
import logging
from typing import Dict, Any
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AIAnalysisService:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    async def analyze_deal(self, deal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a real estate deal using AI and provide predictive insights
        
        Args:
            deal: Dictionary containing deal information
            
        Returns:
            Dictionary with AI analysis results
        """
        try:
            # Create system message for the AI
            system_message = """You are an expert real estate investment analyst with 20+ years of experience. 
You analyze property deals and provide data-driven insights on investment potential, risks, and opportunities.
Always respond with a valid JSON object following this exact structure:

{
    "ai_confidence_score": <number 0-100>,
    "prediction": "<bullish/bearish/neutral>",
    "key_insights": [
        "<insight 1>",
        "<insight 2>",
        "<insight 3>"
    ],
    "risk_factors": [
        {
            "factor": "<risk name>",
            "severity": "<low/medium/high>",
            "description": "<brief description>"
        }
    ],
    "opportunities": [
        {
            "opportunity": "<opportunity name>",
            "potential": "<low/medium/high>",
            "description": "<brief description>"
        }
    ],
    "recommendations": [
        "<recommendation 1>",
        "<recommendation 2>",
        "<recommendation 3>"
    ],
    "market_outlook": "<brief market outlook>",
    "investment_strategy": "<best strategy for this deal>"
}"""

            # Initialize chat with unique session
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"deal-analysis-{deal.get('id', 'unknown')}",
                system_message=system_message
            ).with_model("openai", "gpt-4o-mini")
            
            # Prepare deal data for analysis
            deal_summary = self._prepare_deal_summary(deal)
            
            # Create analysis prompt
            prompt = f"""Analyze this real estate investment opportunity and provide a comprehensive assessment:

PROPERTY DETAILS:
- Address: {deal.get('address', 'Not specified')}
- Property Type: {deal.get('property_type', 'Not specified')}
- Purchase Price: ${deal.get('price', 0):,.2f}
- After Repair Value (ARV): ${deal.get('arv', 0):,.2f}
- Estimated Rehab: ${deal.get('estimated_rehab', 0):,.2f}

FINANCIAL METRICS:
- Deal Score (Traditional): {deal.get('deal_score', 0):.1f}/100
- Cap Rate: {deal.get('cap_rate', 0):.2f}%
- Cash-on-Cash Return: {deal.get('cash_on_cash_pct', 0):.2f}%
- Monthly Cash Flow: ${deal.get('monthly_cashflow', 0):,.2f}
- NOI: ${deal.get('noi', 0):,.2f}
- Gross Annual Income: ${deal.get('gross_income_annual', 0):,.2f}
- Operating Expenses: ${deal.get('operating_expenses', 0):,.2f}

INVESTMENT STRUCTURE:
- Down Payment: ${deal.get('down_payment_amount', 0):,.2f}
- Loan Amount: ${deal.get('loan_amount', 0):,.2f}
- Monthly Mortgage: ${deal.get('monthly_mortgage', 0):,.2f}

PROPERTY SPECS:
- Square Feet: {deal.get('sqft', 0):,.0f}
- Bedrooms: {deal.get('beds', 'N/A')}
- Bathrooms: {deal.get('baths', 'N/A')}
- Units: {deal.get('units', 1)}
- Occupancy: {deal.get('occupancy_pct', 0):.1f}%

CURRENT RECOMMENDATION: {deal.get('preferred_strategy', 'Not specified')}

Provide a comprehensive AI-powered analysis in valid JSON format only. Consider market trends, financial health, investment potential, and hidden opportunities or risks."""

            # Send message and get response
            user_message = UserMessage(text=prompt)
            response = await chat.send_message(user_message)
            
            # Parse JSON response
            try:
                # Extract JSON from response (handle markdown code blocks if present)
                response_text = response.strip()
                if response_text.startswith("```json"):
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif response_text.startswith("```"):
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                ai_analysis = json.loads(response_text)
                
                # Add metadata
                ai_analysis['analyzed_at'] = 'now'
                ai_analysis['model'] = 'gpt-4o-mini'
                ai_analysis['deal_id'] = deal.get('id')
                
                return ai_analysis
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                logger.error(f"Raw response: {response}")
                # Return fallback analysis
                return self._fallback_analysis(deal)
                
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return self._fallback_analysis(deal)
    
    def _prepare_deal_summary(self, deal: Dict[str, Any]) -> str:
        """Prepare a concise deal summary for AI analysis"""
        return f"""
Property: {deal.get('address', 'Unknown')}
Type: {deal.get('property_type', 'Unknown')}
Price: ${deal.get('price', 0):,.0f}
Score: {deal.get('deal_score', 0):.1f}
Cap Rate: {deal.get('cap_rate', 0):.2f}%
Cash Flow: ${deal.get('monthly_cashflow', 0):,.0f}/mo
"""
    
    def _fallback_analysis(self, deal: Dict[str, Any]) -> Dict[str, Any]:
        """Provide fallback analysis if AI fails"""
        score = deal.get('deal_score', 0)
        cap_rate = deal.get('cap_rate', 0)
        cash_flow = deal.get('monthly_cashflow', 0)
        
        # Determine prediction based on metrics
        if score >= 70 and cap_rate >= 8:
            prediction = "bullish"
            confidence = 75
        elif score >= 50 and cap_rate >= 6:
            prediction = "neutral"
            confidence = 60
        else:
            prediction = "bearish"
            confidence = 45
        
        return {
            "ai_confidence_score": confidence,
            "prediction": prediction,
            "key_insights": [
                f"Traditional deal score is {score:.1f}/100",
                f"Cap rate of {cap_rate:.2f}% indicates {'strong' if cap_rate >= 8 else 'moderate' if cap_rate >= 6 else 'weak'} returns",
                f"Monthly cash flow of ${cash_flow:,.0f} {'positive' if cash_flow > 0 else 'negative'}"
            ],
            "risk_factors": [
                {
                    "factor": "Market Volatility",
                    "severity": "medium",
                    "description": "Standard market risks apply to this property type"
                }
            ],
            "opportunities": [
                {
                    "opportunity": "Value-Add Potential",
                    "potential": "medium",
                    "description": "Property may benefit from improvements"
                }
            ],
            "recommendations": [
                "Conduct thorough due diligence before proceeding",
                "Verify all financial assumptions with local market data",
                "Consider engaging a local real estate professional"
            ],
            "market_outlook": "Market conditions require careful analysis",
            "investment_strategy": deal.get('preferred_strategy', 'hold'),
            "analyzed_at": "now",
            "model": "fallback",
            "deal_id": deal.get('id')
        }
