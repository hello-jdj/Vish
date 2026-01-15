from typing import List, Dict

class BashContext:
    def __init__(self):
        self.variables: Dict[str, str] = {}
        self.indent_level = 0
        self.lines: List[str] = []
        self.function_lines = []
        self.emitted_nodes = set()
        self._current_buffer = "main"
    
    def add_line(self, line: str):
        indent = "    " * self.indent_level
        if self._current_buffer == "function":
            self.function_lines.append(f"{indent}{line}")
        else:
            self.lines.append(f"{indent}{line}")

    def add_function_line(self, line: str):
        self.function_lines.append(line)

    def build(self) -> str:
        return "\n".join(self.function_lines + [""] + self.lines)
    
    def indent(self):
        self.indent_level += 1
    
    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)
    
    def get_script(self) -> str:
        return "\n".join(self.function_lines + [""] + self.lines)
