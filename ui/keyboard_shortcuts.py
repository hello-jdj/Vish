from core.traduction import Traduction
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

class KeyboardShortcutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(Traduction.get_trad("keyboard_shortcuts", "Keyboard Shortcuts"))
        self.setMinimumSize(400, 300)

        # TODO: Add actual shortcuts and their descriptions        
