from PySide6.QtGui import QUndoCommand
from core.graph import Graph, Node, Edge

class AddNodeCommand(QUndoCommand):
    def __init__(self, graph: Graph, node: Node, graph_view):
        super().__init__("Add Node")
        self.graph = graph
        self.node = node
        self.graph_view = graph_view
    
    def redo(self):
        self.graph.add_node(self.node)
        self.graph_view.add_node_item(self.node)
    
    def undo(self):
        self.graph.remove_node(self.node.id)
        self.graph_view.remove_node_item(self.node.id)

class RemoveNodeCommand(QUndoCommand):
    def __init__(self, graph: Graph, node_id: str, graph_view):
        super().__init__("Remove Node")
        self.graph = graph
        self.node_id = node_id
        self.node = graph.nodes.get(node_id)
        self.graph_view = graph_view
        self.edges = []
    
    def redo(self):
        node = self.graph.nodes.get(self.node_id)
        if node:
            for port in node.inputs + node.outputs:
                self.edges.extend([(e.id, e.source.id, e.target.id) for e in port.connected_edges[:]])
        self.graph.remove_node(self.node_id)
        self.graph_view.remove_node_item(self.node_id)
    
    def undo(self):
        self.graph.add_node(self.node)
        self.graph_view.add_node_item(self.node)
        for edge_id, source_id, target_id in self.edges:
            pass

class AddEdgeCommand(QUndoCommand):
    def __init__(self, graph: Graph, edge: Edge, graph_view):
        super().__init__("Add Connection")
        self.graph = graph
        self.edge = edge
        self.graph_view = graph_view
    
    def redo(self):
        self.graph.edges[self.edge.id] = self.edge
        self.graph_view.add_edge_item(self.edge)
    
    def undo(self):
        self.graph.remove_edge(self.edge.id)
        if self.edge.id in self.graph_view.edge_items:
            edge_item = self.graph_view.edge_items[self.edge.id]
            self.graph_view.graph_scene.removeItem(edge_item)
            del self.graph_view.edge_items[self.edge.id]

class MoveNodeCommand(QUndoCommand):
    def __init__(self, node: Node, old_pos, new_pos):
        super().__init__("Move Node")
        self.node = node
        self.old_pos = old_pos
        self.new_pos = new_pos
    
    def redo(self):
        self.node.x = self.new_pos.x()
        self.node.y = self.new_pos.y()
    
    def undo(self):
        self.node.x = self.old_pos.x()
        self.node.y = self.old_pos.y()