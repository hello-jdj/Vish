from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainter
from core.graph import Graph, Port
from .graph_scene import GraphScene
from .node_item import NodeItem
from .edge_item import EdgeItem

class GraphView(QGraphicsView):
    connection_request = Signal(Port, Port)
    
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.graph_scene = GraphScene(self.graph)
        self.setScene(self.graph_scene)
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.dragging_edge = None
        self.drag_start_port = None
        self.node_items = {}
        self.edge_items = {}
        
        self.scale_factor = 1.0
    
    def add_node_item(self, node):
        node_item = NodeItem(node)
        node_item.setPos(node.x, node.y)
        self.graph_scene.addItem(node_item)
        self.node_items[node.id] = node_item
        return node_item
    
    def add_edge_item(self, edge):
        edge_item = EdgeItem(edge)
        self.graph_scene.addItem(edge_item)
        self.edge_items[edge.id] = edge_item
        self.update_edge_item(edge_item)
        return edge_item
    
    def update_edge_item(self, edge_item):
        source_node_item = self.node_items.get(edge_item.edge.source.node.id)
        target_node_item = self.node_items.get(edge_item.edge.target.node.id)
        
        if source_node_item and target_node_item:
            source_pos = source_node_item.get_port_scene_pos(edge_item.edge.source.id)
            target_pos = target_node_item.get_port_scene_pos(edge_item.edge.target.id)
            edge_item.set_positions(source_pos, target_pos)
    
    def update_all_edges(self):
        for edge_item in self.edge_items.values():
            self.update_edge_item(edge_item)
    
    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
            self.scale_factor *= zoom_factor
        else:
            zoom_factor = zoom_out_factor
            self.scale_factor *= zoom_factor
        
        if 0.2 <= self.scale_factor <= 3.0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale_factor /= zoom_factor

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fake_event = event.clone()
            fake_event.button = Qt.LeftButton
            super().mousePressEvent(fake_event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.graph_scene.selectedItems():
                if isinstance(item, NodeItem):
                    self.remove_node_item(item.node.id)
        super().keyPressEvent(event)

    def remove_node_item(self, node_id):
        if node_id not in self.node_items:
            return

        node_item = self.node_items[node_id]

        # supprimer edges visuels
        for edge in list(self.graph_scene.edges):
            if (edge.source_port in node_item.port_items.values() or
                edge.target_port in node_item.port_items.values()):
                self.graph_scene.removeItem(edge)
                self.graph_scene.edges.remove(edge)

        self.graph_scene.removeItem(node_item)
        del self.node_items[node_id]
