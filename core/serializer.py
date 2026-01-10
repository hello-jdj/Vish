import json
from typing import Dict, Any
from .graph import Graph, Node, Port

class Serializer:
    VERSION = "1.0.0"
    
    @staticmethod
    def serialize(graph: Graph) -> str:
        data = {
            "version": Serializer.VERSION,
            "nodes": [],
            "edges": []
        }
        
        for node in graph.nodes.values():
            node_data = {
                "id": node.id,
                "type": node.node_type,
                "title": node.title,
                "x": node.x,
                "y": node.y,
                "properties": node.properties,
                "inputs": [{"id": p.id, "name": p.name, "type": p.port_type.value} for p in node.inputs],
                "outputs": [{"id": p.id, "name": p.name, "type": p.port_type.value} for p in node.outputs]
            }
            data["nodes"].append(node_data)
        
        for edge in graph.edges.values():
            edge_data = {
                "id": edge.id,
                "source": edge.source.id,
                "target": edge.target.id
            }
            data["edges"].append(edge_data)
        
        return json.dumps(data, indent=2)
    
    @staticmethod
    def deserialize(json_str: str, node_factory) -> Graph:
        data = json.loads(json_str)
        graph = Graph()
        
        port_map = {}
        
        for node_data in data["nodes"]:
            node = node_factory.create_node(node_data["type"])
            node.id = node_data["id"]
            node.title = node_data["title"]
            node.x = node_data["x"]
            node.y = node_data["y"]
            node.properties = node_data.get("properties", {})
            graph.add_node(node)
            
            for port in node.inputs + node.outputs:
                port_map[port.id] = port
        
        for edge_data in data["edges"]:
            source = port_map.get(edge_data["source"])
            target = port_map.get(edge_data["target"])
            if source and target:
                graph.add_edge(source, target)
        
        return graph