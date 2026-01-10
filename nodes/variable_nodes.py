from core.port_types import PortType
from core.bash_emitter import BashContext
from .base_node import BaseNode

class SetVariableNode(BaseNode):
    def __init__(self):
        super().__init__("set_variable", "Set Variable", "#F39C12")
        self.add_input("Exec", PortType.EXEC)
        self.add_input("Value", PortType.STRING)
        self.add_output("Exec", PortType.EXEC)
        self.properties["variable"] = "VAR"
        self.properties["value"] = ""
    
    def emit_bash(self, context: BashContext) -> str:
        var_name = self.properties.get("variable", "VAR")
        value = self.properties.get("value", "")
        
        value_port = self.inputs[1]
        if value_port.connected_edges:
            source_node = value_port.connected_edges[0].source.node
            value = source_node.properties.get("value", value)
        
        context.variables[var_name] = value
        return f'{var_name}="{value}"'

class GetVariableNode(BaseNode):
    def __init__(self):
        super().__init__("get_variable", "Get Variable", "#F39C12")
        self.add_output("Value", PortType.VARIABLE)
        self.properties["variable"] = "VAR"
    
    def emit_bash(self, context: BashContext) -> str:
        var_name = self.properties.get("variable", "VAR")
        return f"${var_name}"

class FileExistsNode(BaseNode):
    def __init__(self):
        super().__init__("file_exists", "File Exists", "#1ABC9C")
        self.add_input("Path", PortType.PATH)
        self.add_output("Result", PortType.STRING)
        self.properties["path"] = ""
    
    def emit_bash(self, context: BashContext) -> str:
        path = self.properties.get("path", "")
        
        path_port = self.inputs[0]
        if path_port.connected_edges:
            source_node = path_port.connected_edges[0].source.node
            path = source_node.properties.get("value", path)
        
        return f'-f "{path}"'