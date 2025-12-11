# MCP Real Estate Mega Workflow - Connection Guide

## Overview
This document describes the properly connected workflow for the MCP Real Estate system, showing how all nodes are interconnected to process real estate transactions from start to finish.

## Workflow Architecture

### Node Connections Diagram

```
Redwood RCP (Trigger)
    ↓
Auto Check (Validation)
    ↓
Switch Canonical (Decision)
    ├─→ Return Auth Failed (if auth fails)
    └─→ Call SGDT Material Finaltech (if auth succeeds)
            ↓
        Call SGDT Property Camp
            ↓
        Call SGDT Claiming Reserve
            ├─→ Return G24 Response
            │       ↓
            └─→ Call SGDT Lead Upload
                    ↓
                Call SGDT Lead-In System
                    ↓
                Call SGDT-Offer Compare
                    ↓
                Call SGDT Compact Services Transfer
                    ↓
                Call SGDT Compact Minerations
                    ↓
                Call SGDT M-S-General
                    ↓
                Call SGDT Client Creation Selection
                    ↓
                Return Initialized Confirmed

(Any Error) → Logged Error → Return Error
```

## Node Descriptions

### 1. Redwood RCP (Trigger)
- **Type**: Trigger
- **Purpose**: Entry point for the workflow
- **Outputs**: Auto Check
- **Description**: Initiates the real estate processing workflow

### 2. Auto Check (Validation)
- **Type**: Validation
- **Purpose**: Validates incoming data and authentication
- **Inputs**: Redwood RCP
- **Outputs**: Switch Canonical
- **Description**: Performs initial validation of request data

### 3. Switch Canonical (Decision)
- **Type**: Decision
- **Purpose**: Routes workflow based on authentication status
- **Inputs**: Auto Check
- **Outputs**:
  - Return Auth Failed (if authentication fails)
  - Call SGDT Material Finaltech (if authentication succeeds)
- **Description**: Makes routing decision based on authentication

### 4. Return Auth Failed (Return)
- **Type**: Return
- **Purpose**: Terminates workflow with auth failure
- **Inputs**: Switch Canonical
- **Outputs**: None (terminal node)
- **Description**: Returns authentication failure response

### 5. Call SGDT Material Finaltech (API Call)
- **Type**: API Call
- **Purpose**: Retrieves material and financial tech data
- **Inputs**: Switch Canonical
- **Outputs**: Call SGDT Property Camp
- **Description**: First API call in the SGDT service chain

### 6. Call SGDT Property Camp (API Call)
- **Type**: API Call
- **Purpose**: Processes property campaign data
- **Inputs**: Call SGDT Material Finaltech
- **Outputs**: Call SGDT Claiming Reserve
- **Description**: Handles property campaign processing

### 7. Call SGDT Claiming Reserve (API Call)
- **Type**: API Call
- **Purpose**: Manages claiming and reservation processes
- **Inputs**: Call SGDT Property Camp
- **Outputs**: Return G24 Response, Call SGDT Lead Upload
- **Description**: Processes property claims and reservations

### 8. Return G24 Response (API Call)
- **Type**: API Call
- **Purpose**: Provides G24 system response
- **Inputs**: Call SGDT Claiming Reserve
- **Outputs**: Call SGDT Lead Upload
- **Description**: Returns G24 integration response

### 9. Call SGDT Lead Upload (API Call)
- **Type**: API Call
- **Purpose**: Uploads lead information
- **Inputs**: Call SGDT Claiming Reserve, Return G24 Response
- **Outputs**: Call SGDT Lead-In System
- **Description**: Uploads processed lead data

### 10. Call SGDT Lead-In System (API Call)
- **Type**: API Call
- **Purpose**: Integrates lead into main system
- **Inputs**: Call SGDT Lead Upload
- **Outputs**: Call SGDT-Offer Compare
- **Description**: Processes lead integration

### 11. Call SGDT-Offer Compare (API Call)
- **Type**: API Call
- **Purpose**: Compares available offers
- **Inputs**: Call SGDT Lead-In System
- **Outputs**: Call SGDT Compact Services Transfer
- **Description**: Performs offer comparison analysis

### 12. Call SGDT Compact Services Transfer (API Call)
- **Type**: API Call
- **Purpose**: Transfers compact services data
- **Inputs**: Call SGDT-Offer Compare
- **Outputs**: Call SGDT Compact Minerations
- **Description**: Handles service transfer operations

### 13. Call SGDT Compact Minerations (API Call)
- **Type**: API Call
- **Purpose**: Processes minerations data
- **Inputs**: Call SGDT Compact Services Transfer
- **Outputs**: Call SGDT M-S-General
- **Description**: Handles minerations processing

### 14. Call SGDT M-S-General (API Call)
- **Type**: API Call
- **Purpose**: General M-S system processing
- **Inputs**: Call SGDT Compact Minerations
- **Outputs**: Call SGDT Client Creation Selection
- **Description**: Performs general system operations

### 15. Call SGDT Client Creation Selection (API Call)
- **Type**: API Call
- **Purpose**: Creates and selects client records
- **Inputs**: Call SGDT M-S-General
- **Outputs**: Return Initialized Confirmed
- **Description**: Finalizes client creation

### 16. Return Initialized Confirmed (Return)
- **Type**: Return
- **Purpose**: Returns successful completion
- **Inputs**: Call SGDT Client Creation Selection
- **Outputs**: None (terminal node)
- **Description**: Returns successful workflow completion

### 17. Logged Error (Error Handler)
- **Type**: Error Handler
- **Purpose**: Logs and handles workflow errors
- **Inputs**: Any node (on error)
- **Outputs**: Return Error
- **Description**: Global error handling

### 18. Return Error (Return)
- **Type**: Return
- **Purpose**: Returns error response
- **Inputs**: Logged Error
- **Outputs**: None (terminal node)
- **Description**: Returns error information to caller

## Workflow Execution Flow

### Success Path
1. Workflow starts at **Redwood RCP**
2. Data validated by **Auto Check**
3. **Switch Canonical** checks authentication
4. If authenticated, proceeds through the SGDT service chain:
   - Material Finaltech → Property Camp → Claiming Reserve
   - G24 Response generated
   - Lead Upload → Lead-In System → Offer Compare
   - Compact Services Transfer → Compact Minerations
   - M-S-General → Client Creation Selection
5. Completes with **Return Initialized Confirmed**

### Error Path
- Any node encountering an error routes to **Logged Error**
- **Logged Error** processes and logs the error
- **Return Error** returns error details to caller

### Authentication Failure Path
1. Workflow starts at **Redwood RCP**
2. Data validated by **Auto Check**
3. **Switch Canonical** detects authentication failure
4. Routes directly to **Return Auth Failed**
5. Workflow terminates

## Running the Workflow

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execute Workflow
```bash
python workflow_executor.py
```

### View Workflow Diagram
The executor will automatically print the workflow diagram and execution results.

## Configuration

The workflow is configured in `workflow_config.json`, which defines:
- All nodes and their types
- Connection mappings between nodes
- Error handling configuration
- Retry and timeout settings

## Error Handling

The workflow includes comprehensive error handling:
- **Global Error Handler**: All errors route to "Logged Error"
- **Retry Attempts**: 3 automatic retries for failed operations
- **Timeout**: 30 second timeout per node execution

## Integration Points

### SGDT API Endpoints
The workflow integrates with multiple SGDT (assumed API) endpoints:
- Material Finaltech Service
- Property Camp Service
- Claiming Reserve Service
- Lead Upload Service
- Lead-In System Service
- Offer Compare Service
- Compact Services Transfer
- Compact Minerations
- M-S-General Service
- Client Creation Selection

### External Systems
- **Redwood RCP**: Incoming request system
- **G24 System**: Response integration
- **Authentication Service**: Via Switch Canonical

## Monitoring and Logging

The workflow executor provides:
- Detailed execution logs
- Node-by-node status tracking
- Error tracking and reporting
- Performance metrics (nodes executed, execution time)

## Future Enhancements

Potential improvements to the workflow:
1. Add parallel execution for independent API calls
2. Implement caching for frequently accessed data
3. Add conditional routing based on business rules
4. Implement async/await for better performance
5. Add webhook support for external notifications
