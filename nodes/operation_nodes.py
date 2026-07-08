from nodes.base_node import BaseNode
from core.port_types import PortType
from core.bash_emitter import BashContext
from nodes.registry import register_node

@register_node("math_node_base")
class MathNode(BaseNode):
    def _resolve(self, port, context: BashContext, default="0"):
        if port.connected_edges:
            return port.connected_edges[0].source.node.emit_bash_value(context)
        return default

@register_node("int_constant")
class IntConstant(MathNode):
    def __init__(self):
        super().__init__("int_const", "Int", "#BDC3C7")
        self.add_output("Value", PortType.INT)
        self.properties["value"] = 0

    def emit_bash_value(self, context: BashContext) -> str:
        return str(self.properties.get("value", 0))

@register_node("addition")
class Addition(MathNode):
    def __init__(self):
        super().__init__("addition", "Addition", "#F1C40F")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} + {b}))"

@register_node("subtraction")
class Subtraction(MathNode):
    def __init__(self):
        super().__init__("subtraction", "Subtraction", "#E67E22")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} - {b}))"

@register_node("multiplication")
class Multiplication(MathNode):
    def __init__(self):
        super().__init__("multiplication", "Multiplication", "#9B59B6")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} * {b}))"

@register_node("division")
class Division(MathNode):
    def __init__(self):
        super().__init__("division", "Division", "#3498DB")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} / {b}))"

@register_node("modulo")
class Modulo(MathNode):
    def __init__(self):
        super().__init__("modulo", "Modulo", "#1ABC9C")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} % {b}))"

@register_node("less_than")
class LessThan(MathNode):
    def __init__(self):
        super().__init__("less_than", "Less Than", "#95A5A6")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} < {b}))"

@register_node("greater_than")
class GreaterThan(MathNode):
    def __init__(self):
        super().__init__("greater_than", "Greater Than", "#95A5A6")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} > {b}))"

@register_node("equals")
class Equals(MathNode):
    def __init__(self):
        super().__init__("equals", "Equals", "#2ECC71")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} == {b}))"

@register_node("logical_and")
class LogicalAnd(MathNode):
    def __init__(self):
        super().__init__("logical_and", "AND", "#34495E")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} && {b}))"

@register_node("logical_or")
class LogicalOr(MathNode):
    def __init__(self):
        super().__init__("logical_or", "OR", "#34495E")
        self.add_input("A", PortType.INT)
        self.add_input("B", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        b = self._resolve(self.inputs[1], context)
        return f"$(({a} || {b}))"

@register_node("logical_not")
class LogicalNot(MathNode):
    def __init__(self):
        super().__init__("logical_not", "NOT", "#34495E")
        self.add_input("A", PortType.INT)
        self.add_output("Result", PortType.INT)

    def emit_bash_value(self, context: BashContext) -> str:
        a = self._resolve(self.inputs[0], context)
        return f"$((!{a}))"
