"""
Integrated Workflow Executor
Handles both webhook trigger workflow and the main MCP Real Estate workflow
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NodeType(Enum):
    WEBHOOK_TRIGGER = "webhook_trigger"
    HTTP_REQUEST = "http_request"
    WEBHOOK_RESPONSE = "webhook_response"
    TRIGGER = "trigger"
    VALIDATION = "validation"
    DECISION = "decision"
    API_CALL = "api_call"
    RETURN = "return"
    ERROR_HANDLER = "error_handler"


@dataclass
class NodeResult:
    """Result from executing a workflow node"""
    node_id: str
    success: bool
    data: Any
    next_nodes: List[str]
    error: Optional[str] = None


class IntegratedWorkflowExecutor:
    """Executes integrated workflow system with webhook triggers"""

    def __init__(self, config_path: str = "integrated_workflow_config.json"):
        """Initialize integrated workflow executor"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.nodes = {node['id']: node for node in self.config['nodes']}
        self.connections = self._build_connection_map()
        self.execution_log = []
        self.async_executions = {}

    def _build_connection_map(self) -> Dict[str, List[Dict]]:
        """Build a map of connections from each node"""
        conn_map = {}
        for conn in self.config['connections']:
            from_node = conn['from']
            if from_node not in conn_map:
                conn_map[from_node] = []
            conn_map[from_node].append(conn)
        return conn_map

    def execute_node(self, node_id: str, input_data: Any) -> NodeResult:
        """Execute a single workflow node"""
        node = self.nodes[node_id]
        logger.info(f"Executing node: {node['name']} (ID: {node_id})")

        try:
            node_type = NodeType(node['type'])

            if node_type == NodeType.WEBHOOK_TRIGGER:
                return self._execute_webhook_trigger(node, input_data)
            elif node_type == NodeType.HTTP_REQUEST:
                return self._execute_http_request(node, input_data)
            elif node_type == NodeType.WEBHOOK_RESPONSE:
                return self._execute_webhook_response(node, input_data)
            elif node_type == NodeType.TRIGGER:
                return self._execute_trigger(node, input_data)
            elif node_type == NodeType.VALIDATION:
                return self._execute_validation(node, input_data)
            elif node_type == NodeType.DECISION:
                return self._execute_decision(node, input_data)
            elif node_type == NodeType.API_CALL:
                return self._execute_api_call(node, input_data)
            elif node_type == NodeType.RETURN:
                return self._execute_return(node, input_data)
            elif node_type == NodeType.ERROR_HANDLER:
                return self._execute_error_handler(node, input_data)
            else:
                raise ValueError(f"Unknown node type: {node_type}")

        except Exception as e:
            logger.error(f"Error executing node {node_id}: {str(e)}")
            return NodeResult(
                node_id=node_id,
                success=False,
                data=None,
                next_nodes=['logged_error'],
                error=str(e)
            )

    def _execute_webhook_trigger(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute webhook trigger node"""
        logger.info(f"Webhook Trigger: {node['name']} - Received webhook request")

        webhook_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'webhook',
            'payload': input_data,
            'webhook_id': node['id']
        }

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=webhook_data,
            next_nodes=node['outputs']
        )

    def _execute_http_request(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute HTTP request node (simulated)"""
        logger.info(f"HTTP Request: {node['name']} - Forwarding to workflow engine")

        # Simulate HTTP request to trigger main workflow
        http_response = {
            'status': 200,
            'body': {
                'success': True,
                'workflow_id': 'MCP_RealEstate_MegaWorkflow',
                'execution_id': f"exec_{datetime.now().timestamp()}",
                'message': 'Workflow execution initiated'
            },
            'headers': {
                'Content-Type': 'application/json'
            }
        }

        # Extract data to forward to main workflow
        forwarded_data = {
            **input_data.get('payload', {}),
            'trigger_source': 'http_request',
            'execution_id': http_response['body']['execution_id']
        }

        # Determine next nodes based on connection type
        next_nodes = []
        if node['id'] in self.connections:
            for conn in self.connections[node['id']]:
                next_nodes.append(conn['to'])

        return NodeResult(
            node_id=node['id'],
            success=True,
            data={
                'http_response': http_response,
                'forwarded_data': forwarded_data
            },
            next_nodes=next_nodes
        )

    def _execute_webhook_response(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute webhook response node"""
        logger.info(f"Webhook Response: {node['name']} - Sending response to webhook caller")

        response_data = {
            'status_code': 200,
            'response': {
                'success': True,
                'message': 'Workflow initiated',
                'execution_id': input_data.get('http_response', {}).get('body', {}).get('execution_id'),
                'workflow_id': input_data.get('http_response', {}).get('body', {}).get('workflow_id')
            }
        }

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=response_data,
            next_nodes=[]  # Terminal node for webhook flow
        )

    def _execute_trigger(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute trigger node (main workflow start)"""
        logger.info(f"Trigger: {node['name']} - Starting main workflow")

        # Extract forwarded data from HTTP request
        if isinstance(input_data, dict):
            if 'forwarded_data' in input_data:
                workflow_data = input_data['forwarded_data']
            elif 'http_response' in input_data:
                # Extract from the full HTTP response structure
                workflow_data = input_data.get('forwarded_data', input_data)
            else:
                workflow_data = input_data
        else:
            workflow_data = input_data

        logger.info(f"Trigger data: {workflow_data}")

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=workflow_data,
            next_nodes=node['outputs']
        )

    def _execute_validation(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute validation node"""
        logger.info(f"Validation: {node['name']} - Checking input data")

        # Check if we have valid data in various possible structures
        is_valid = isinstance(input_data, dict) and (
            input_data.get('data') is not None or
            input_data.get('property_id') is not None or
            input_data.get('source') is not None  # For webhook-triggered data
        )

        return NodeResult(
            node_id=node['id'],
            success=is_valid,
            data=input_data,
            next_nodes=node['outputs'] if is_valid else ['logged_error']
        )

    def _execute_decision(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute decision node"""
        logger.info(f"Decision: {node['name']} - Making routing decision")

        auth_status = input_data.get('authenticated', True)  # Default to True for demo

        if auth_status:
            next_nodes = ['call_sgdt_material']
        else:
            next_nodes = ['return_auth_failed']

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=input_data,
            next_nodes=next_nodes
        )

    def _execute_api_call(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute API call node"""
        logger.info(f"API Call: {node['name']} - Calling external service")

        result_data = {
            **input_data,
            'api_response': {
                'node': node['name'],
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
        }

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=result_data,
            next_nodes=node['outputs']
        )

    def _execute_return(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute return node"""
        logger.info(f"Return: {node['name']} - Returning result")

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=input_data,
            next_nodes=[]
        )

    def _execute_error_handler(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute error handler node"""
        logger.error(f"Error Handler: {node['name']} - Handling error")

        error_data = {
            'error': True,
            'original_data': input_data,
            'error_message': input_data.get('error', 'Unknown error'),
            'timestamp': datetime.now().isoformat()
        }

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=error_data,
            next_nodes=node['outputs']
        )

    def execute_integrated_workflow(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete integrated workflow starting from webhook"""
        logger.info(f"Starting integrated workflow: {self.config['name']}")

        # Start with the webhook trigger
        current_nodes = ['webhook_trigger']
        current_data = webhook_data

        visited_nodes = set()
        max_iterations = 100
        iteration = 0

        webhook_response = None
        main_workflow_started = False

        # Track data per node for proper routing
        node_data_map = {'webhook_trigger': webhook_data}

        while current_nodes and iteration < max_iterations:
            iteration += 1
            next_nodes = []

            for node_id in current_nodes:
                # Skip already visited non-error nodes
                if node_id in visited_nodes and node_id != 'logged_error':
                    continue

                visited_nodes.add(node_id)
                node = self.nodes[node_id]

                # Get the appropriate data for this node
                node_input_data = node_data_map.get(node_id, current_data)

                # Execute the node
                result = self.execute_node(node_id, node_input_data)
                self.execution_log.append({
                    'node_id': node_id,
                    'node_name': node['name'],
                    'workflow': node.get('workflow', 'unknown'),
                    'success': result.success,
                    'error': result.error
                })

                # Handle special cases
                if node_id == 'respond_to_webhook':
                    webhook_response = result.data

                if node_id == 'http_request':
                    # HTTP request triggers async main workflow
                    main_workflow_started = True
                    # Route data to different next nodes
                    if result.data and 'forwarded_data' in result.data:
                        # Redwood RCP gets forwarded_data
                        node_data_map['redwood_rcp'] = result.data['forwarded_data']
                        # Respond to webhook gets the HTTP response
                        node_data_map['respond_to_webhook'] = result.data

                # Update data and next nodes
                if result.success:
                    if result.data:
                        current_data = result.data

                    # Add next nodes to processing queue
                    for next_node in result.next_nodes:
                        if next_node not in node_data_map:
                            node_data_map[next_node] = result.data
                    next_nodes.extend(result.next_nodes)
                else:
                    next_nodes.append('logged_error')
                    current_data = {'error': result.error, **current_data}

            current_nodes = next_nodes

        logger.info(f"Integrated workflow completed after {iteration} iterations")
        logger.info(f"Visited {len(visited_nodes)} nodes")

        return {
            'success': True,
            'webhook_response': webhook_response,
            'main_workflow_started': main_workflow_started,
            'final_data': current_data,
            'execution_log': self.execution_log,
            'nodes_executed': len(visited_nodes)
        }

    def get_integration_diagram(self) -> str:
        """Generate integration architecture diagram"""
        diagram = [
            "╔═══════════════════════════════════════════════════════════════════════╗",
            "║           Integrated Real Estate Workflow Architecture               ║",
            "╚═══════════════════════════════════════════════════════════════════════╝",
            "",
            "┌─────────────────────────────────────────────────────────────────────┐",
            "│  WEBHOOK TRIGGER WORKFLOW (Entry Point)                            │",
            "└─────────────────────────────────────────────────────────────────────┘",
            "",
            "   ┏━━━━━━━━━━━━━┓",
            "   ┃  Webhook    ┃ ◄─── External POST request",
            "   ┗━━━━━━━━━━━━━┛",
            "         │",
            "         ▼",
            "   ┏━━━━━━━━━━━━━┓",
            "   ┃ HTTP Request┃ ──┐",
            "   ┗━━━━━━━━━━━━━┛   │",
            "         │            │",
            "         │            └──── Async Trigger ────┐",
            "         ▼                                     │",
            "   ┌──────────────┐                            │",
            "   │  Respond to  │                            │",
            "   │   Webhook    │ ──► Returns 200 OK         │",
            "   └──────────────┘     (Immediate Response)   │",
            "                                                │",
            "┌───────────────────────────────────────────────┼──────────────────┐",
            "│  MCP REAL ESTATE MEGAWORKFLOW (Main Process) │                  │",
            "└───────────────────────────────────────────────┼──────────────────┘",
            "                                                │",
            "                                                ▼",
            "                                         ┏━━━━━━━━━━━━━┓",
            "                                         ┃ Redwood RCP ┃",
            "                                         ┗━━━━━━━━━━━━━┛",
            "                                                │",
            "                                                ▼",
            "                                         ┏━━━━━━━━━━━━━┓",
            "                                         ┃ Auto Check  ┃",
            "                                         ┗━━━━━━━━━━━━━┛",
            "                                                │",
            "                                                ▼",
            "                                         ┏━━━━━━━━━━━━━━━┓",
            "                                         ┃ Switch        ┃",
            "                                         ┃ Canonical     ┃",
            "                                         ┗━━━━━━━━━━━━━━━┛",
            "                                                │",
            "                                   ┌────────────┴────────────┐",
            "                                   │                         │",
            "                            [Auth Failed]              [Auth Success]",
            "                                   │                         │",
            "                                   ▼                         ▼",
            "                          ┌──────────────┐         ┏━━━━━━━━━━━━━━━━━┓",
            "                          │Return Auth   │         ┃ SGDT Material   ┃",
            "                          │   Failed     │         ┃ Finaltech       ┃",
            "                          └──────────────┘         ┗━━━━━━━━━━━━━━━━━┛",
            "                                                           │",
            "                                                           ▼",
            "                                              [12 SGDT API Calls Chain]",
            "                                                           │",
            "                                                           ▼",
            "                                                  ┌──────────────────┐",
            "                                                  │ Return           │",
            "                                                  │ Initialized      │",
            "                                                  │ Confirmed        │",
            "                                                  └──────────────────┘",
            "",
            "┌─────────────────────────────────────────────────────────────────────┐",
            "│  ERROR HANDLING (Global)                                           │",
            "└─────────────────────────────────────────────────────────────────────┘",
            "",
            "   [Any Error] ──► ┏━━━━━━━━━━━━━━┓ ──► ┌──────────────┐",
            "                   ┃ Logged Error ┃     │ Return Error │",
            "                   ┗━━━━━━━━━━━━━━┛     └──────────────┘",
            "",
            "═══════════════════════════════════════════════════════════════════════",
            "KEY INTEGRATION POINTS:",
            "  1. Webhook receives external POST request",
            "  2. HTTP Request forwards data and triggers main workflow",
            "  3. Webhook Response returns immediately (async pattern)",
            "  4. Main workflow processes in background",
            "  5. Global error handler catches all failures",
            "═══════════════════════════════════════════════════════════════════════"
        ]

        return "\n".join(diagram)


def main():
    """Main execution function"""
    executor = IntegratedWorkflowExecutor()

    # Print integration diagram
    print(executor.get_integration_diagram())
    print("\n" + "=" * 80 + "\n")

    # Simulate webhook request
    webhook_request = {
        'data': 'real_estate_property_data',
        'authenticated': True,
        'property_id': 'PROP-WEBHOOK-12345',
        'customer_id': 'CUST-WEBHOOK-67890',
        'source': 'external_api'
    }

    logger.info("Simulating webhook POST request...")
    result = executor.execute_integrated_workflow(webhook_request)

    # Print results
    print("\n" + "=" * 80)
    print("INTEGRATED WORKFLOW EXECUTION RESULTS")
    print("=" * 80)
    print(f"Overall Success: {result['success']}")
    print(f"Main Workflow Started: {result['main_workflow_started']}")
    print(f"Nodes Executed: {result['nodes_executed']}")

    if result['webhook_response']:
        print(f"\nWebhook Response:")
        print(f"  Status: {result['webhook_response']['status_code']}")
        print(f"  Execution ID: {result['webhook_response']['response'].get('execution_id')}")

    print("\n" + "-" * 80)
    print("EXECUTION LOG:")
    print("-" * 80)

    current_workflow = None
    for log_entry in result['execution_log']:
        workflow = log_entry['workflow']
        if workflow != current_workflow:
            current_workflow = workflow
            print(f"\n[{workflow.upper()}]")

        status = "✓" if log_entry['success'] else "✗"
        print(f"  {status} {log_entry['node_name']}")
        if log_entry['error']:
            print(f"    Error: {log_entry['error']}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
