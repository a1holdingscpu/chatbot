"""
Workflow Visualizer
Generates visual representations of the workflow connections
"""

import json
from typing import Dict, List, Set


class WorkflowVisualizer:
    """Creates visual representations of workflow connections"""

    def __init__(self, config_path: str = "workflow_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.nodes = {node['id']: node for node in self.config['nodes']}
        self.connections = self._build_connection_map()

    def _build_connection_map(self) -> Dict[str, List[Dict]]:
        """Build a map of connections from each node"""
        conn_map = {}
        for conn in self.config['connections']:
            from_node = conn['from']
            if from_node not in conn_map:
                conn_map[from_node] = []
            conn_map[from_node].append(conn)
        return conn_map

    def generate_ascii_diagram(self) -> str:
        """Generate detailed ASCII art workflow diagram"""
        lines = []
        lines.append("╔" + "═" * 78 + "╗")
        lines.append("║" + f"{self.config['name']:^78}" + "║")
        lines.append("╚" + "═" * 78 + "╝")
        lines.append("")

        # Main flow
        lines.append("┌─ MAIN WORKFLOW FLOW ─────────────────────────────────────────────────┐")
        lines.append("│                                                                       │")
        lines.append("│  ┏━━━━━━━━━━━━━━━━━━┓                                               │")
        lines.append("│  ┃  Redwood RCP     ┃ ◄── Entry Point                               │")
        lines.append("│  ┗━━━━━━━━━━━━━━━━━━┛                                               │")
        lines.append("│          │                                                           │")
        lines.append("│          ▼                                                           │")
        lines.append("│  ┏━━━━━━━━━━━━━━━━━━┓                                               │")
        lines.append("│  ┃   Auto Check     ┃ ◄── Validation                                │")
        lines.append("│  ┗━━━━━━━━━━━━━━━━━━┛                                               │")
        lines.append("│          │                                                           │")
        lines.append("│          ▼                                                           │")
        lines.append("│  ┏━━━━━━━━━━━━━━━━━━┓                                               │")
        lines.append("│  ┃ Switch Canonical ┃ ◄── Decision Point                            │")
        lines.append("│  ┗━━━━━━━━━━━━━━━━━━┛                                               │")
        lines.append("│          │                                                           │")
        lines.append("│          ├─────────────┐                                            │")
        lines.append("│          │             │                                            │")
        lines.append("│   [Auth Failed]   [Auth Success]                                    │")
        lines.append("│          │             │                                            │")
        lines.append("│          ▼             ▼                                            │")
        lines.append("│  ┌──────────────┐  ┏━━━━━━━━━━━━━━━━━━━━━━┓                        │")
        lines.append("│  │ Return Auth  │  ┃ SGDT Material        ┃                        │")
        lines.append("│  │    Failed    │  ┃ Finaltech            ┃                        │")
        lines.append("│  └──────────────┘  ┗━━━━━━━━━━━━━━━━━━━━━━┛                        │")
        lines.append("│                               │                                      │")
        lines.append("│                               ▼                                      │")
        lines.append("│                    ┏━━━━━━━━━━━━━━━━━━━━━━┓                        │")
        lines.append("│                    ┃ SGDT Property Camp   ┃                        │")
        lines.append("│                    ┗━━━━━━━━━━━━━━━━━━━━━━┛                        │")
        lines.append("│                               │                                      │")
        lines.append("│                               ▼                                      │")
        lines.append("│                    ┏━━━━━━━━━━━━━━━━━━━━━━┓                        │")
        lines.append("│                    ┃ SGDT Claiming        ┃                        │")
        lines.append("│                    ┃ Reserve              ┃                        │")
        lines.append("│                    ┗━━━━━━━━━━━━━━━━━━━━━━┛                        │")
        lines.append("│                               │                                      │")
        lines.append("│                               ├──────────┐                          │")
        lines.append("│                               │          │                          │")
        lines.append("│                               ▼          ▼                          │")
        lines.append("│                    ┌──────────────┐  ┌──────────────┐              │")
        lines.append("│                    │ Return G24   │  │ SGDT Lead    │              │")
        lines.append("│                    │  Response    │──│   Upload     │              │")
        lines.append("│                    └──────────────┘  └──────────────┘              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┏━━━━━━━━━━━━━━━━━┓              │")
        lines.append("│                                   ┃ SGDT Lead-In    ┃              │")
        lines.append("│                                   ┃ System          ┃              │")
        lines.append("│                                   ┗━━━━━━━━━━━━━━━━━┛              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┏━━━━━━━━━━━━━━━━━┓              │")
        lines.append("│                                   ┃ SGDT Offer      ┃              │")
        lines.append("│                                   ┃ Compare         ┃              │")
        lines.append("│                                   ┗━━━━━━━━━━━━━━━━━┛              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┏━━━━━━━━━━━━━━━━━┓              │")
        lines.append("│                                   ┃ SGDT Compact    ┃              │")
        lines.append("│                                   ┃ Services        ┃              │")
        lines.append("│                                   ┗━━━━━━━━━━━━━━━━━┛              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┏━━━━━━━━━━━━━━━━━┓              │")
        lines.append("│                                   ┃ SGDT Compact    ┃              │")
        lines.append("│                                   ┃ Minerations     ┃              │")
        lines.append("│                                   ┗━━━━━━━━━━━━━━━━━┛              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┏━━━━━━━━━━━━━━━━━┓              │")
        lines.append("│                                   ┃ SGDT M-S        ┃              │")
        lines.append("│                                   ┃ General         ┃              │")
        lines.append("│                                   ┗━━━━━━━━━━━━━━━━━┛              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┏━━━━━━━━━━━━━━━━━┓              │")
        lines.append("│                                   ┃ SGDT Client     ┃              │")
        lines.append("│                                   ┃ Creation        ┃              │")
        lines.append("│                                   ┗━━━━━━━━━━━━━━━━━┛              │")
        lines.append("│                                              │                       │")
        lines.append("│                                              ▼                       │")
        lines.append("│                                   ┌──────────────────┐              │")
        lines.append("│                                   │ Return           │              │")
        lines.append("│                                   │ Initialized      │              │")
        lines.append("│                                   │ Confirmed        │              │")
        lines.append("│                                   └──────────────────┘              │")
        lines.append("│                                                                       │")
        lines.append("└───────────────────────────────────────────────────────────────────┘")
        lines.append("")
        lines.append("┌─ ERROR HANDLING ─────────────────────────────────────────────────────┐")
        lines.append("│                                                                       │")
        lines.append("│   [Any Error] ──► ┏━━━━━━━━━━━━━━┓ ──► ┌──────────────┐           │")
        lines.append("│                   ┃ Logged Error ┃     │ Return Error │           │")
        lines.append("│                   ┗━━━━━━━━━━━━━━┛     └──────────────┘           │")
        lines.append("│                                                                       │")
        lines.append("└───────────────────────────────────────────────────────────────────┘")
        lines.append("")
        lines.append("Legend:")
        lines.append("  ┏━━━━━┓  Processing Node")
        lines.append("  ┌─────┐  Terminal Node")
        lines.append("  ──►     Connection Flow")

        return "\n".join(lines)

    def generate_connection_matrix(self) -> str:
        """Generate a connection matrix showing all node relationships"""
        node_ids = [node['id'] for node in self.config['nodes']]

        lines = []
        lines.append("\nConnection Matrix:")
        lines.append("=" * 80)

        # Create header
        header = "FROM \\ TO".ljust(30)
        for node_id in node_ids[:5]:  # Show first 5 for readability
            header += node_id[:8].ljust(10)
        lines.append(header + "...")
        lines.append("-" * 80)

        # Create matrix rows
        for from_node_id in node_ids:
            row = from_node_id[:28].ljust(30)
            for to_node_id in node_ids[:5]:
                # Check if connection exists
                has_connection = False
                if from_node_id in self.connections:
                    for conn in self.connections[from_node_id]:
                        if conn['to'] == to_node_id:
                            has_connection = True
                            break
                row += ("✓" if has_connection else "·").ljust(10)
            lines.append(row + "...")

        return "\n".join(lines)

    def generate_detailed_connections(self) -> str:
        """Generate detailed list of all connections"""
        lines = []
        lines.append("\nDetailed Connection List:")
        lines.append("=" * 80)

        for node in self.config['nodes']:
            node_id = node['id']
            lines.append(f"\n📦 {node['name']} (ID: {node_id})")
            lines.append(f"   Type: {node['type']}")

            # Show incoming connections
            incoming = []
            for other_node_id, conns in self.connections.items():
                # Skip wildcard connections
                if other_node_id == '*':
                    continue
                for conn in conns:
                    if conn['to'] == node_id:
                        from_name = self.nodes.get(other_node_id, {}).get('name', other_node_id)
                        incoming.append({
                            'from': from_name,
                            'condition': conn.get('condition', 'always')
                        })

            if incoming:
                lines.append("   ⬅ Inputs:")
                for inc in incoming:
                    lines.append(f"      • {inc['from']} (when: {inc['condition']})")
            else:
                lines.append("   ⬅ Inputs: None (entry point)")

            # Show outgoing connections
            if node_id in self.connections:
                lines.append("   ➡ Outputs:")
                for conn in self.connections[node_id]:
                    to_node = self.nodes[conn['to']]
                    condition = conn.get('condition', 'always')
                    lines.append(f"      • {to_node['name']} (when: {condition})")
            else:
                lines.append("   ➡ Outputs: None (terminal node)")

        return "\n".join(lines)

    def validate_connections(self) -> Dict[str, List[str]]:
        """Validate workflow connections and return any issues"""
        issues = {
            'errors': [],
            'warnings': [],
            'info': []
        }

        # Check for disconnected nodes
        connected_nodes = set()
        for node_id in self.connections:
            connected_nodes.add(node_id)
            for conn in self.connections[node_id]:
                connected_nodes.add(conn['to'])

        all_nodes = set(self.nodes.keys())
        disconnected = all_nodes - connected_nodes

        if disconnected:
            issues['warnings'].append(f"Disconnected nodes: {disconnected}")

        # Check for terminal nodes (no outputs)
        terminal_nodes = []
        for node_id, node in self.nodes.items():
            if node_id not in self.connections or not self.connections[node_id]:
                terminal_nodes.append(node['name'])

        issues['info'].append(f"Terminal nodes: {', '.join(terminal_nodes)}")

        # Check for entry points (no inputs)
        entry_nodes = []
        all_targets = set()
        for conns in self.connections.values():
            for conn in conns:
                all_targets.add(conn['to'])

        for node_id in self.nodes:
            if node_id not in all_targets:
                entry_nodes.append(self.nodes[node_id]['name'])

        issues['info'].append(f"Entry points: {', '.join(entry_nodes)}")

        return issues


def main():
    """Main function to generate all visualizations"""
    visualizer = WorkflowVisualizer()

    print(visualizer.generate_ascii_diagram())
    print("\n" + "=" * 80 + "\n")
    print(visualizer.generate_connection_matrix())
    print("\n" + "=" * 80 + "\n")
    print(visualizer.generate_detailed_connections())
    print("\n" + "=" * 80 + "\n")

    # Validate connections
    issues = visualizer.validate_connections()
    print("\n🔍 Connection Validation:")
    print("=" * 80)

    if issues['errors']:
        print("\n❌ Errors:")
        for error in issues['errors']:
            print(f"   • {error}")

    if issues['warnings']:
        print("\n⚠️  Warnings:")
        for warning in issues['warnings']:
            print(f"   • {warning}")

    if issues['info']:
        print("\n ℹ️  Info:")
        for info in issues['info']:
            print(f"   • {info}")

    if not issues['errors']:
        print("\n✅ All connections are valid!")


if __name__ == "__main__":
    main()
