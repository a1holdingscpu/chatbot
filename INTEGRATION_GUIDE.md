# Webhook Integration Guide

## Overview

This document explains how the **Webhook Trigger Workflow** integrates with the **MCP Real Estate MegaWorkflow** to create a complete, production-ready real estate processing system.

## Architecture Pattern

The integration follows an **Async Trigger Pattern** where:
1. External webhook request arrives
2. System immediately acknowledges with 200 OK
3. Main workflow processes asynchronously in the background

## Integration Components

### Component 1: Webhook Trigger Workflow (Entry Point)

```
┏━━━━━━━━━━━━━┓      ┏━━━━━━━━━━━━━┓      ┌──────────────┐
┃  Webhook    ┃ ───► ┃ HTTP Request┃ ───► │  Respond to  │
┗━━━━━━━━━━━━━┛      ┗━━━━━━━━━━━━━┛      │   Webhook    │
                            │              └──────────────┘
                            │
                            └──── Triggers Main Workflow
```

**Nodes:**
- **Webhook**: Listens for incoming POST requests at `/webhook/real-estate`
- **HTTP Request**: Forwards data to workflow engine and triggers main workflow
- **Respond to Webhook**: Returns immediate 200 OK response to caller

**Purpose:** Provides external API interface for triggering the real estate workflow

### Component 2: MCP Real Estate MegaWorkflow (Main Processor)

```
Redwood RCP → Auto Check → Switch Canonical → [SGDT API Chain] → Return
```

**Purpose:** Processes real estate transactions through 12 SGDT API integrations

## How They Work Together

### 1. Request Flow

```
External System
    │
    │ POST /webhook/real-estate
    │ {property_data, customer_id, ...}
    ▼
┌─────────────────────────────────────────┐
│  WEBHOOK TRIGGER WORKFLOW               │
│                                         │
│  1. Webhook receives request            │
│  2. HTTP Request forwards to engine     │
│  3. Respond returns 200 OK immediately  │
└─────────────────────────────────────────┘
                    │
                    │ Async Trigger
                    ▼
┌─────────────────────────────────────────┐
│  MCP REAL ESTATE MEGAWORKFLOW           │
│                                         │
│  1. Redwood RCP starts processing       │
│  2. Auto Check validates data           │
│  3. Switch Canonical routes by auth     │
│  4. 12 SGDT API calls execute           │
│  5. Return Initialized Confirmed        │
└─────────────────────────────────────────┘
```

### 2. Data Flow

```yaml
External Request:
  property_id: "PROP-12345"
  customer_id: "CUST-67890"
  property_data: {...}

↓ Webhook Trigger

Webhook Data:
  timestamp: "2025-12-11T..."
  source: "webhook"
  payload: {external request}

↓ HTTP Request

Forwarded Data:
  property_id: "PROP-12345"
  customer_id: "CUST-67890"
  trigger_source: "http_request"
  execution_id: "exec_1234567890"

↓ Redwood RCP (Main Workflow)

Workflow Processing Data:
  {all forwarded data}
  + api_responses from each SGDT call
```

### 3. Response Pattern

**Immediate Response (from Webhook Workflow):**
```json
{
  "success": true,
  "message": "Workflow initiated",
  "workflow_id": "MCP_RealEstate_MegaWorkflow",
  "execution_id": "exec_1234567890"
}
```

**Async Processing Result (from Main Workflow):**
```json
{
  "workflow_completed": true,
  "final_status": "initialized_confirmed",
  "sgdt_responses": [...],
  "execution_id": "exec_1234567890"
}
```

## Integration Benefits

### 1. **Separation of Concerns**

- **Webhook Workflow**: Handles HTTP communication, authentication, request/response
- **Main Workflow**: Focuses purely on business logic and SGDT integrations

### 2. **Async Processing**

- External callers don't wait for the entire workflow
- Immediate acknowledgment improves user experience
- Background processing scales independently

### 3. **Modularity**

- Each workflow can be tested independently
- Main workflow can be triggered from multiple sources:
  - Webhooks
  - Scheduled jobs
  - Internal API calls
  - Manual triggers

### 4. **Error Isolation**

- Webhook errors (network, auth) handled separately
- Main workflow errors don't affect webhook response
- Global error handler catches issues from both workflows

## Configuration Files

### 1. `webhook_workflow_config.json`

Defines the webhook trigger workflow independently:
- Webhook listener configuration
- HTTP request forwarding
- Response templates

### 2. `integrated_workflow_config.json`

Combines both workflows with proper connections:
- All nodes from both workflows
- Cross-workflow connections
- Integration architecture settings

### 3. `workflow_config.json` (Original)

Maintains the standalone MCP workflow for direct execution

## Execution Modes

### Mode 1: Webhook-Triggered (Production)

```bash
python integrated_workflow_executor.py
```

**Use Case:** External systems triggering via HTTP POST

**Flow:** Webhook → HTTP → Main Workflow

### Mode 2: Direct Execution (Testing/Internal)

```bash
python workflow_executor.py
```

**Use Case:** Internal triggers, testing, scheduled jobs

**Flow:** Main Workflow only

## Key Integration Points

### Point 1: HTTP Request → Redwood RCP

```json
{
  "from": "http_request",
  "to": "redwood_rcp",
  "type": "workflow_trigger",
  "async": true
}
```

This connection bridges the two workflows:
- HTTP Request completes in Webhook Workflow
- Data forwarded to Redwood RCP in Main Workflow
- Async flag allows independent execution

### Point 2: Data Mapping

```json
"trigger_mapping": {
  "webhook.body.property_data": "redwood_rcp.input.data",
  "webhook.body.customer_id": "redwood_rcp.input.customer_id",
  "webhook.headers.authorization": "auto_check.auth_token"
}
```

Maps webhook fields to main workflow inputs

### Point 3: Shared Error Handler

```json
{
  "id": "logged_error",
  "workflow": "both",
  "inputs": ["*"]
}
```

Global error handler catches failures from both workflows

## Real-World Usage

### Example: External Real Estate Platform Integration

```python
# External system calls webhook
import requests

response = requests.post(
    'https://your-domain.com/webhook/real-estate',
    json={
        'property_id': 'PROP-12345',
        'customer_id': 'CUST-67890',
        'property_data': {
            'address': '123 Main St',
            'price': 500000,
            'type': 'residential'
        },
        'authenticated': True
    },
    headers={
        'Authorization': 'Bearer YOUR_API_TOKEN'
    }
)

# Immediate response received
print(response.json())
# {
#   "success": true,
#   "execution_id": "exec_1234567890",
#   "message": "Workflow initiated"
# }

# Main workflow processes in background
# Results available via execution_id query or callback webhook
```

## Monitoring & Observability

### Execution Logs

Both workflows provide detailed logs:

```
[WEBHOOK_TRIGGER]
  ✓ Webhook
  ✓ HTTP Request
  ✓ Respond to Webhook

[MCP_REALESTATE_MEGAWORKFLOW]
  ✓ Redwood RCP
  ✓ Auto Check
  ✓ Switch Canonical
  ✓ Call SGDT Material Finaltech
  ... (12 more SGDT calls)
  ✓ Return Initialized Confirmed
```

### Metrics to Track

1. **Webhook Workflow**:
   - Request rate
   - Response time (should be < 100ms)
   - Authentication failures
   - Trigger success rate

2. **Main Workflow**:
   - Total execution time
   - SGDT API success rates
   - Error rates per node
   - Completion rate

## Testing

### Unit Testing

```python
# Test webhook workflow only
executor = IntegratedWorkflowExecutor()
result = executor.execute_node('webhook_trigger', test_data)

# Test main workflow only
executor = WorkflowExecutor()
result = executor.execute_workflow(test_data)
```

### Integration Testing

```python
# Test complete flow
executor = IntegratedWorkflowExecutor()
result = executor.execute_integrated_workflow(webhook_request)

assert result['webhook_response']['status_code'] == 200
assert result['main_workflow_started'] == True
assert result['success'] == True
```

## Deployment Considerations

### 1. Scaling

- **Webhook Workflow**: Scale horizontally for high request volume
- **Main Workflow**: Scale based on SGDT API capacity
- Consider queue-based architecture for very high volumes

### 2. Security

- Implement webhook authentication (API keys, signatures)
- Validate all incoming data
- Rate limiting on webhook endpoint
- Secure SGDT API credentials

### 3. Reliability

- Retry logic for failed SGDT calls
- Dead letter queue for failed workflows
- Monitoring and alerting
- Idempotency for retries

## Migration Path

### From Standalone to Integrated

1. **Phase 1**: Deploy both standalone and webhook workflows
2. **Phase 2**: Test webhook triggers in staging
3. **Phase 3**: Migrate production traffic to webhook endpoint
4. **Phase 4**: Keep standalone for internal/scheduled jobs

## Summary

The webhook integration provides:

✅ **External API Interface** - RESTful endpoint for triggering workflows
✅ **Async Processing** - Immediate response with background execution
✅ **Modularity** - Independent workflows that work together
✅ **Scalability** - Components scale independently
✅ **Flexibility** - Multiple trigger methods supported
✅ **Production Ready** - Error handling, logging, monitoring built-in

The integration maintains the robustness of the original MCP Real Estate workflow while adding a modern webhook-based interface for external systems.
