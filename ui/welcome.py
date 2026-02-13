from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QInputDialog,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from ui.menu_style import apply_btn_style
from core.traduction import Traduction
from core.projects import ProjectManager

class WelcomeScreen(QDialog):
    def __init__(self, parent, project_manager: ProjectManager):
        super().__init__(parent)

        self.project_manager = project_manager

        self.setWindowTitle(Traduction.get_trad("welcome_title", "Welcome"))
        self.setModal(True)
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        title = QLabel(Traduction.get_trad("welcome_recent_projects", "Recent Projects"))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.recent_list = QListWidget()
        self.recent_list.addItems(self.project_manager.get_recent_projects())
        self.recent_list.itemDoubleClicked.connect(self.open_recent)
        layout.addWidget(self.recent_list)
        self.new_btn = QPushButton(
            Traduction.get_trad("welcome_new_project", "New Project")
        )
        apply_btn_style(self.new_btn)
        self.new_btn.clicked.connect(self.create_project)
        layout.addWidget(self.new_btn)
        self.open_btn = QPushButton(
            Traduction.get_trad("welcome_open_project", "Open Project")
        )
        apply_btn_style(self.open_btn)
        self.open_btn.clicked.connect(self.open_project)
        layout.addWidget(self.open_btn)

    def create_project(self):
        name, ok = QInputDialog.getText(
            self,
            Traduction.get_trad("new_project_name", "Project Name"),
            Traduction.get_trad("new_project_enter_name", "Enter project name:")
        )

        if not ok or not name.strip():
            return
        base_dir = Path(self.project_manager.config_dir) / "projects"
        project_dir = base_dir / name

        try:
            self.project_manager.create_project(project_dir, name)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_project(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            Traduction.get_trad("select_project_folder", "Select Project Folder")
        )

        if not directory:
            return

        try:
            self.project_manager.load_project(Path(directory))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_recent(self, item):
        try:
            self.project_manager.load_project(Path(item.text()))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
