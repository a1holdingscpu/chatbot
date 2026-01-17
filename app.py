from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

def calculate_lead_score(lead_data):
    """
    Calculate a lead score based on various criteria.
    Score ranges from 0-100.
    """
    score = 0

    # Email domain scoring
    email = lead_data.get('email', '')
    if email:
        domain = email.split('@')[-1].lower()
        business_domains = ['company.com', 'corp.com', 'business.com']
        if any(bd in domain for bd in business_domains):
            score += 20
        elif not any(free in domain for free in ['gmail', 'yahoo', 'hotmail', 'outlook']):
            score += 10

    # Company size scoring
    company_size = lead_data.get('company_size', '').lower()
    size_scores = {
        'enterprise': 30,
        'large': 25,
        'medium': 20,
        'small': 15,
        'startup': 10
    }
    score += size_scores.get(company_size, 0)

    # Budget scoring
    budget = lead_data.get('budget', 0)
    if budget >= 100000:
        score += 25
    elif budget >= 50000:
        score += 20
    elif budget >= 25000:
        score += 15
    elif budget >= 10000:
        score += 10
    elif budget > 0:
        score += 5

    # Industry scoring
    industry = lead_data.get('industry', '').lower()
    high_value_industries = ['technology', 'finance', 'healthcare', 'manufacturing']
    if any(ind in industry for ind in high_value_industries):
        score += 15

    # Job title scoring
    job_title = lead_data.get('job_title', '').lower()
    decision_maker_titles = ['ceo', 'cto', 'cfo', 'vp', 'director', 'head', 'manager']
    if any(title in job_title for title in decision_maker_titles):
        score += 10

    # Engagement scoring
    engagement = lead_data.get('engagement_level', '').lower()
    engagement_scores = {
        'high': 10,
        'medium': 5,
        'low': 2
    }
    score += engagement_scores.get(engagement, 0)

    # Cap at 100
    return min(score, 100)

def get_lead_quality(score):
    """Categorize lead quality based on score"""
    if score >= 80:
        return 'Hot'
    elif score >= 60:
        return 'Warm'
    elif score >= 40:
        return 'Cold'
    else:
        return 'Unqualified'

@app.route('/webhook-test/crm-lead-score', methods=['POST', 'GET'])
def crm_lead_score():
    """
    Webhook endpoint for CRM lead scoring.
    Accepts lead data and returns a calculated score.
    """
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'message': 'CRM Lead Scoring Webhook is active',
            'endpoint': '/webhook-test/crm-lead-score',
            'methods': ['POST'],
            'expected_fields': {
                'email': 'string',
                'company_size': 'string (enterprise|large|medium|small|startup)',
                'budget': 'number',
                'industry': 'string',
                'job_title': 'string',
                'engagement_level': 'string (high|medium|low)',
                'first_name': 'string (optional)',
                'last_name': 'string (optional)',
                'company_name': 'string (optional)',
                'phone': 'string (optional)'
            }
        }), 200

    try:
        # Get JSON data from request
        lead_data = request.get_json() or {}

        # Calculate lead score
        score = calculate_lead_score(lead_data)
        quality = get_lead_quality(score)

        # Prepare response
        response = {
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat(),
            'lead_data': {
                'email': lead_data.get('email', 'N/A'),
                'company_name': lead_data.get('company_name', 'N/A'),
                'first_name': lead_data.get('first_name', 'N/A'),
                'last_name': lead_data.get('last_name', 'N/A')
            },
            'scoring': {
                'score': score,
                'quality': quality,
                'max_score': 100
            },
            'recommendations': []
        }

        # Add recommendations based on score
        if quality == 'Hot':
            response['recommendations'].append('Immediate follow-up recommended')
            response['recommendations'].append('Assign to senior sales representative')
        elif quality == 'Warm':
            response['recommendations'].append('Follow-up within 24 hours')
            response['recommendations'].append('Send targeted product information')
        elif quality == 'Cold':
            response['recommendations'].append('Add to nurture campaign')
            response['recommendations'].append('Send educational content')
        else:
            response['recommendations'].append('Add to general newsletter list')
            response['recommendations'].append('Monitor engagement for 30 days')

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 400

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'name': 'Pulseboard Agency - CRM Lead Scoring API',
        'version': '1.0.0',
        'description': 'Webhook service for scoring CRM leads based on multiple criteria',
        'endpoints': {
            '/': 'API documentation (this page)',
            '/webhook-test/crm-lead-score': 'POST endpoint for lead scoring',
            '/health': 'Health check endpoint'
        },
        'status': 'active'
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Pulseboard Agency - CRM Lead Scoring Service")
    print("📍 Server running on http://localhost:5678")
    print("🔗 Webhook endpoint: http://localhost:5678/webhook-test/crm-lead-score")
    app.run(host='0.0.0.0', port=5678, debug=True)
