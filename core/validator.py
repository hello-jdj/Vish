from core.port_types import PortDirection

class GraphValidator:
    @staticmethod
    def is_valid_connection(graph, existing_edges, a, b) -> bool:
        if a is b:
            return False

        if a.port.node.id == b.port.node.id:
            return False

        if a.is_input == b.is_input:
            return False

        if a.port.port_type != b.port.port_type:
            return False

        if a.port.direction == PortDirection.OUTPUT:
            src = a.port
            dst = b.port
        else:
            src = b.port
            dst = a.port

        if GraphValidator._can_reach(graph, dst.node, src.node):
            return False

        for edge in existing_edges:
            if edge.target_port is (b if b.is_input else a):
                return False

        return True

    @staticmethod
    def _can_reach(graph, start_node, target_node) -> bool:
        visited = set()

        def dfs(node):
            if node.id in visited:
                return False
            visited.add(node.id)

            if node is target_node:
                return True

            for edge in graph.edges.values():
                if edge.source.node is node:
                    if dfs(edge.target.node):
                        return True
            return False

        return dfs(start_node)