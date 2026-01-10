from enum import Enum
from dataclasses import dataclass
from typing import Any

class PortType(Enum):
    EXEC = "exec"
    STRING = "string"
    INT = "int"
    BOOL = "bool"
    PATH = "path"
    VARIABLE = "variable"

class PortDirection(Enum):
    INPUT = "input"
    OUTPUT = "output"

@dataclass
class PortStyle:
    color: str
    size: int
    
EXEC_STYLE = PortStyle("#FFFFFF", 12)
STRING_STYLE = PortStyle("#FF6B9D", 10)
INT_STYLE = PortStyle("#4ECDC4", 10)
BOOL_STYLE = PortStyle("#95E1D3", 10)
PATH_STYLE = PortStyle("#F38181", 10)
VARIABLE_STYLE = PortStyle("#FFA07A", 10)

PORT_STYLES = {
    PortType.EXEC: EXEC_STYLE,
    PortType.STRING: STRING_STYLE,
    PortType.INT: INT_STYLE,
    PortType.BOOL: BOOL_STYLE,
    PortType.PATH: PATH_STYLE,
    PortType.VARIABLE: VARIABLE_STYLE,
}