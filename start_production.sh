#!/bin/bash

# Pulseboard Agency - Production Startup Script

echo "🚀 Starting Pulseboard Agency CRM Lead Scoring Service (Production Mode)"
echo "📍 Server will run on http://0.0.0.0:5678"
echo "🔗 Webhook endpoint: http://localhost:5678/webhook-test/crm-lead-score"
echo ""

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null
then
    echo "❌ Gunicorn is not installed. Installing..."
    pip install gunicorn
fi

# Start Gunicorn with config
echo "✅ Starting Gunicorn server..."
gunicorn --config gunicorn_config.py app:app
