from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit
)

class PropertyPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setMinimumWidth(250)
        self.current_node = None

    def set_node(self, node):
        self.clear()
        self.current_node = node

        if not node:
            return

        self.layout.addWidget(QLabel(f"<b>{node.title}</b>"))

        for key, value in node.properties.items():
            label = QLabel(key)
            field = QLineEdit(str(value))

            field.textChanged.connect(
                lambda v, k=key: self._update_property(k, v)
            )

            self.layout.addWidget(label)
            self.layout.addWidget(field)

        self.layout.addStretch()

    def _update_property(self, key, value):
        if self.current_node:
            self.current_node.properties[key] = value

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
