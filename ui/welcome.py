from pathlib import Path
import json
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QInputDialog,
    QFileDialog, QMessageBox, QListWidgetItem,
    QWidget, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.menu_style import apply_btn_style
from core.traduction import Traduction
from core.projects import ProjectManager
from theme.theme import Theme

class WelcomeScreen(QDialog):
    def __init__(self, parent, project_manager: ProjectManager):
        super().__init__(parent)

        self.project_manager = project_manager

        self.setWindowTitle("  ")
        self.setModal(True)
        self.setMinimumSize(650, 500)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Theme.BACKGROUND};
            }}
            QLabel {{
                color: {Theme.TEXT};
                background: transparent;
            }}
            QListWidget {{
                background-color: {Theme.PANEL};
                border-radius: 8px;
                padding: 6px;
                color: {Theme.TEXT};
            }}
            QListWidget::item {{
                padding: 10px;
                border-radius: 6px;
            }}
            QListWidget::item:selected {{
                background-color: {Theme.BUTTON};
            }}
            QListWidget::item:hover {{
                background-color: {Theme.BUTTON_HOVER};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel(Traduction.get_trad("welcome_title", "Welcome"))
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {Theme.TEXT}; background: transparent; font-size: 18pt;")

        main_layout.addWidget(title)

        recent_label = QLabel(
            Traduction.get_trad("welcome_recent_projects", "Recent Projects")
        )
        recent_label.setStyleSheet(f"color: {Theme.TEXT}; font-weight: bold;")
        main_layout.addWidget(recent_label)

        self.recent_list = QListWidget()
        self.recent_list.itemDoubleClicked.connect(self.open_recent)
        main_layout.addWidget(self.recent_list)

        self.populate_recent_projects()

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)
        button_container.setStyleSheet("background: transparent;")

        self.new_btn = QPushButton(
            Traduction.get_trad("welcome_new_project", "New Project")
        )
        apply_btn_style(self.new_btn)
        self.new_btn.clicked.connect(self.create_project)

        self.open_btn = QPushButton(
            Traduction.get_trad("welcome_open_project", "Open Project")
        )
        apply_btn_style(self.open_btn)
        self.open_btn.clicked.connect(self.open_project)

        self.open_btn.setStyleSheet(f"QPushButton:hover {{ background-color: {Theme.BUTTON_HOVER}; }}")
        self.new_btn.setStyleSheet(f"QPushButton:hover {{ background-color: {Theme.BUTTON_HOVER}; }}")

        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.open_btn)

        main_layout.addWidget(button_container)

    def populate_recent_projects(self):
        self.recent_list.clear()

        recents = self.project_manager.get_recent_projects()

        for path_str in recents:
            path = Path(path_str)
            project_file = path / "project.json"

            project_name = path.name

            if project_file.exists():
                try:
                    data = json.loads(project_file.read_text())
                    project_name = data.get("name", path.name)
                except Exception:
                    pass

            item = QListWidgetItem(project_name)
            item.setData(Qt.UserRole, path_str)
            self.recent_list.addItem(item)

    def create_project(self):
        name, ok = QInputDialog.getText(
            self,
            Traduction.get_trad("new_project_name", "Project Name"),
            Traduction.get_trad("new_project_enter_name", "Enter project name:")
        )

        if not ok or not name.strip():
            return
        base_dir = Path(self.project_manager.config_dir) / "projects"
        project_dir = base_dir / name.strip()

        try:
            self.project_manager.create_project(project_dir, name.strip())
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
        path = item.data(Qt.UserRole)

        try:
            self.project_manager.load_project(Path(path))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
