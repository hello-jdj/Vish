from typing import Optional, Tuple
from .graph import Port, Edge

class ValidationError:
    def __init__(self, message: str):
        self.message = message

class Validator:
    @staticmethod
    def validate_connection(source: Port, target: Port) -> Optional[ValidationError]:
        if source.direction == target.direction:
            return ValidationError("Cannot connect same direction ports")
        
        if source.port_type != target.port_type:
            if not (source.port_type.value == "exec" and target.port_type.value == "exec"):
                return ValidationError(f"Type mismatch: {source.port_type.value} → {target.port_type.value}")
        
        if source.direction.value == "input":
            source, target = target, source
        
        if target.port_type.value == "exec":
            pass
        else:
            if target.is_connected():
                return ValidationError("Input already connected")
        
        return None