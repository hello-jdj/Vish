from abc import abstractmethod
from core.graph import Node
from core.bash_emitter import BashContext

class BaseNode(Node):
    def __init__(self, node_type: str, title: str, color: str):
        super().__init__(node_type, title)
        self.color = color
    
    @abstractmethod
    def emit_bash(self, context: BashContext) -> str:
        pass