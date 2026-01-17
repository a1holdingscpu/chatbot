# 🎯 Pulseboard Agency - CRM Lead Scoring Service

A powerful webhook service for scoring and qualifying CRM leads based on multiple criteria including company size, budget, industry, job title, and engagement level.

## Features

- **Intelligent Lead Scoring**: Automatically calculates lead scores (0-100) based on multiple weighted factors
- **Quality Classification**: Categorizes leads as Hot, Warm, Cold, or Unqualified
- **Actionable Recommendations**: Provides specific follow-up recommendations for each lead quality tier
- **RESTful API**: Simple webhook endpoint for easy integration with CRM systems
- **Real-time Processing**: Instant lead scoring and classification

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The service will start on `http://localhost:5678`

## API Endpoints

### 1. Lead Scoring Webhook
**Endpoint**: `POST /webhook-test/crm-lead-score`

Submit lead data to receive a calculated score and quality classification.

**Request Body**:
```json
{
  "email": "john.doe@techcorp.com",
  "company_size": "enterprise",
  "budget": 150000,
  "industry": "technology",
  "job_title": "CTO",
  "engagement_level": "high",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "TechCorp Inc",
  "phone": "+1-555-0100"
}
```

**Response**:
```json
{
  "status": "success",
  "timestamp": "2026-01-17T17:20:03.848345",
  "lead_data": {
    "email": "john.doe@techcorp.com",
    "company_name": "TechCorp Inc",
    "first_name": "John",
    "last_name": "Doe"
  },
  "scoring": {
    "score": 100,
    "quality": "Hot",
    "max_score": 100
  },
  "recommendations": [
    "Immediate follow-up recommended",
    "Assign to senior sales representative"
  ]
}
```

### 2. Webhook Information
**Endpoint**: `GET /webhook-test/crm-lead-score`

Get information about the webhook endpoint and expected fields.

### 3. API Documentation
**Endpoint**: `GET /`

Returns API overview and available endpoints.

### 4. Health Check
**Endpoint**: `GET /health`

Check service availability and health status.

## Scoring Criteria

The lead scoring algorithm evaluates the following factors:

### Email Domain (0-20 points)
- Business domain: 20 points
- Professional domain (non-free): 10 points
- Free email services: 0 points

### Company Size (0-30 points)
- Enterprise: 30 points
- Large: 25 points
- Medium: 20 points
- Small: 15 points
- Startup: 10 points

### Budget (0-25 points)
- $100,000+: 25 points
- $50,000-$99,999: 20 points
- $25,000-$49,999: 15 points
- $10,000-$24,999: 10 points
- $1-$9,999: 5 points

### Industry (0-15 points)
High-value industries receive 15 points:
- Technology
- Finance
- Healthcare
- Manufacturing

### Job Title (0-10 points)
Decision-maker titles receive 10 points:
- CEO, CTO, CFO, COO
- VP/Vice President
- Director
- Head of Department
- Manager

### Engagement Level (0-10 points)
- High: 10 points
- Medium: 5 points
- Low: 2 points

## Quality Classifications

### 🔥 Hot Leads (80-100 points)
- **Action**: Immediate follow-up
- **Assignment**: Senior sales representative
- **Priority**: Highest

### 🌡️ Warm Leads (60-79 points)
- **Action**: Follow-up within 24 hours
- **Assignment**: Sales team
- **Priority**: High

### ❄️ Cold Leads (40-59 points)
- **Action**: Add to nurture campaign
- **Assignment**: Marketing automation
- **Priority**: Medium

### 📊 Unqualified Leads (<40 points)
- **Action**: Newsletter subscription
- **Assignment**: Marketing general list
- **Priority**: Low

## Example Usage

### Using cURL

```bash
# Test with a high-quality lead
curl -X POST http://localhost:5678/webhook-test/crm-lead-score \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah@enterprise.com",
    "company_size": "enterprise",
    "budget": 200000,
    "industry": "technology",
    "job_title": "VP of Sales",
    "engagement_level": "high",
    "first_name": "Sarah",
    "last_name": "Johnson",
    "company_name": "Enterprise Solutions Inc"
  }'
```

### Using Python

```python
import requests

lead_data = {
    "email": "contact@company.com",
    "company_size": "medium",
    "budget": 50000,
    "industry": "finance",
    "job_title": "Director of Operations",
    "engagement_level": "medium",
    "first_name": "Michael",
    "last_name": "Smith",
    "company_name": "Financial Services Co"
}

response = requests.post(
    'http://localhost:5678/webhook-test/crm-lead-score',
    json=lead_data
)

result = response.json()
print(f"Lead Score: {result['scoring']['score']}")
print(f"Quality: {result['scoring']['quality']}")
```

### Using JavaScript/Node.js

```javascript
const axios = require('axios');

const leadData = {
  email: 'info@startup.io',
  company_size: 'startup',
  budget: 15000,
  industry: 'technology',
  job_title: 'founder',
  engagement_level: 'high',
  first_name: 'Alex',
  last_name: 'Chen',
  company_name: 'Startup Innovations'
};

axios.post('http://localhost:5678/webhook-test/crm-lead-score', leadData)
  .then(response => {
    console.log('Score:', response.data.scoring.score);
    console.log('Quality:', response.data.scoring.quality);
    console.log('Recommendations:', response.data.recommendations);
  })
  .catch(error => console.error('Error:', error));
```

## Integration with CRM Systems

### Salesforce Integration
Use Process Builder or Flow to send lead data to the webhook when a new lead is created.

### HubSpot Integration
Configure workflow automation to POST lead data to the webhook endpoint.

### Custom CRM Integration
Send a POST request to `/webhook-test/crm-lead-score` whenever a new lead is captured.

## Development

### Project Structure

```
chatbot/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── streamlit_app.py       # Original chatbot app
├── PULSEBOARD_README.md   # This documentation
└── README.md              # Original README
```

### Running in Development Mode

The application runs in debug mode by default for development:

```bash
python app.py
```

### Running in Production

For production deployments, use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5678 app:app
```

## Testing

### Manual Testing

Test the webhook with various lead profiles:

```bash
# Hot Lead
curl -X POST http://localhost:5678/webhook-test/crm-lead-score \
  -H "Content-Type: application/json" \
  -d '{"email":"ceo@enterprise.com","company_size":"enterprise","budget":500000,"industry":"technology","job_title":"CEO","engagement_level":"high"}'

# Cold Lead
curl -X POST http://localhost:5678/webhook-test/crm-lead-score \
  -H "Content-Type: application/json" \
  -d '{"email":"user@gmail.com","company_size":"small","budget":5000,"industry":"retail","job_title":"employee","engagement_level":"low"}'
```

### Health Check

```bash
curl http://localhost:5678/health
```

## Configuration

You can customize the scoring algorithm by modifying the following in `app.py`:

- **Score weights**: Adjust points for each criterion
- **Industry categories**: Add/remove high-value industries
- **Job title keywords**: Modify decision-maker title patterns
- **Quality thresholds**: Change score ranges for Hot/Warm/Cold classifications

## Security Considerations

For production use, consider adding:

- API key authentication
- Rate limiting
- HTTPS/TLS encryption
- Request validation and sanitization
- CORS configuration
- Logging and monitoring

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please open an issue on the GitHub repository.

---

Built with ❤️ using Flask
