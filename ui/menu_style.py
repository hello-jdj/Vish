from theme.theme import Theme
import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

def apply_menu_style(menu):
    menu.setStyleSheet(f"""
        QMenu {{
            background-color: {Theme.BACKGROUND};
            color: {Theme.TEXT};
            border-radius: 12px;
            padding: 8px;
            border: 1px solid {Theme.BUTTON_PRESSED};
            font-size: 14px;
        }}

        QMenu::item {{
            padding: 10px 22px;
            border-radius: 8px;
            min-width: 150px;
        }}

        QMenu::item:selected {{
            background-color: {Theme.BUTTON_HOVER};
        }}

        QMenu::separator {{
            height: 1px;
            background: {Theme.BUTTON_PRESSED};
            margin: 8px 10px;
        }}
    """)



def apply_btn_style(btn):
    btn.setStyleSheet(f"""
        QToolButton {{
            color: {Theme.TEXT};
            font-size: 18px;
            padding: 4px 8px;
            border-radius: 8px;
        }}
        QToolButton:hover {{
            background-color: {Theme.BUTTON_HOVER};
        }}
        QToolButton::menu-indicator {{
            image: none;
        }}
    """)

def get_icon(name):
    theme = Theme.selected_theme
    if theme == "dark":
        path = os.path.join("assets", "icons", "dark", "menu", f"{name}.png")
        if os.path.exists(path):
            return QIcon(path)
    elif theme == "white":
        path = os.path.join("assets", "icons", "light","menu", f"{name}.png")
        if os.path.exists(path):           
            return QIcon(path)
    return None

def apply_icon_for_btn(btn, name):
    icon = get_icon(name)
    if icon:
        pixmap = icon.pixmap(100, 100)
        btn.setIcon(QIcon(pixmap))