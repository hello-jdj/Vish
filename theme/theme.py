class Theme:
    BACKGROUND = None
    TEXT = None
    LINE = None

def set_dark_theme():
    Theme.BACKGROUND = "#2A2A2A"
    Theme.TEXT = "#FFFFFF"
    Theme.LINE = "#444444"

def set_light_theme():
    Theme.BACKGROUND = "#FFFFFF"
    Theme.TEXT = "#000000"
    Theme.LINE = "#CCCCCC"
