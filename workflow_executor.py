"""
MCP Real Estate Mega Workflow Executor
This module executes the workflow defined in workflow_config.json with proper node connections.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NodeType(Enum):
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


class WorkflowExecutor:
    """Executes workflow based on configuration with proper node connections"""

    def __init__(self, config_path: str = "workflow_config.json"):
        """Initialize workflow executor with configuration"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.nodes = {node['id']: node for node in self.config['nodes']}
        self.connections = self._build_connection_map()
        self.execution_log = []

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

            if node_type == NodeType.TRIGGER:
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

    def _execute_trigger(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute trigger node (workflow start)"""
        logger.info(f"Trigger: {node['name']} - Starting workflow")
        return NodeResult(
            node_id=node['id'],
            success=True,
            data=input_data,
            next_nodes=node['outputs']
        )

    def _execute_validation(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute validation node (Auto Check)"""
        logger.info(f"Validation: {node['name']} - Checking input data")

        # Validate input data structure
        is_valid = isinstance(input_data, dict) and input_data.get('data') is not None

        return NodeResult(
            node_id=node['id'],
            success=is_valid,
            data=input_data,
            next_nodes=node['outputs'] if is_valid else ['logged_error']
        )

    def _execute_decision(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute decision node (Switch Canonical)"""
        logger.info(f"Decision: {node['name']} - Making routing decision")

        # Check authentication status
        auth_status = input_data.get('authenticated', False)

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

        # Simulate API call
        # In production, this would make actual HTTP requests to SGDT services
        result_data = {
            **input_data,
            'api_response': {
                'node': node['name'],
                'status': 'success',
                'timestamp': 'current_time'
            }
        }

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=result_data,
            next_nodes=node['outputs']
        )

    def _execute_return(self, node: Dict, input_data: Any) -> NodeResult:
        """Execute return node (workflow end)"""
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
            'error_message': input_data.get('error', 'Unknown error')
        }

        return NodeResult(
            node_id=node['id'],
            success=True,
            data=error_data,
            next_nodes=node['outputs']
        )

    def execute_workflow(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete workflow from start to finish"""
        logger.info(f"Starting workflow: {self.config['name']}")

        # Start with the trigger node
        current_nodes = ['redwood_rcp']
        current_data = initial_data

        visited_nodes = set()
        max_iterations = 100  # Prevent infinite loops
        iteration = 0

        while current_nodes and iteration < max_iterations:
            iteration += 1
            next_nodes = []

            for node_id in current_nodes:
                # Prevent infinite loops by tracking visited nodes
                if node_id in visited_nodes and node_id != 'logged_error':
                    continue

                visited_nodes.add(node_id)

                # Execute the node
                result = self.execute_node(node_id, current_data)
                self.execution_log.append({
                    'node_id': node_id,
                    'node_name': self.nodes[node_id]['name'],
                    'success': result.success,
                    'error': result.error
                })

                # Update data for next nodes
                if result.success:
                    current_data = result.data
                    next_nodes.extend(result.next_nodes)
                else:
                    # On error, route to error handler
                    next_nodes.append('logged_error')
                    current_data = {'error': result.error, **current_data}

            current_nodes = next_nodes

        logger.info(f"Workflow completed after {iteration} iterations")
        logger.info(f"Visited {len(visited_nodes)} nodes")

        return {
            'success': True,
            'final_data': current_data,
            'execution_log': self.execution_log,
            'nodes_executed': len(visited_nodes)
        }

    def get_workflow_diagram(self) -> str:
        """Generate a text-based workflow diagram showing connections"""
        diagram = [f"Workflow: {self.config['name']}", "=" * 60, ""]

        for node in self.config['nodes']:
            node_id = node['id']
            node_name = node['name']
            node_type = node['type']

            diagram.append(f"[{node_id}] {node_name} ({node_type})")

            # Show connections
            if node_id in self.connections:
                for conn in self.connections[node_id]:
                    to_node = self.nodes[conn['to']]
                    condition = conn.get('condition', 'always')
                    diagram.append(f"  └─> {to_node['name']} (when: {condition})")

            diagram.append("")

        return "\n".join(diagram)


def main():
    """Main execution function"""
    # Initialize workflow executor
    executor = WorkflowExecutor()

    # Print workflow diagram
    print(executor.get_workflow_diagram())
    print("\n" + "=" * 60 + "\n")

    # Execute workflow with sample data
    initial_data = {
        'data': 'sample_property_data',
        'authenticated': True,
        'property_id': 'PROP-12345',
        'customer_id': 'CUST-67890'
    }

    result = executor.execute_workflow(initial_data)

    # Print results
    print("Workflow Execution Results:")
    print(f"Success: {result['success']}")
    print(f"Nodes Executed: {result['nodes_executed']}")
    print("\nExecution Log:")
    for log_entry in result['execution_log']:
        status = "✓" if log_entry['success'] else "✗"
        print(f"  {status} {log_entry['node_name']}")
        if log_entry['error']:
            print(f"    Error: {log_entry['error']}")


if __name__ == "__main__":
    main()
