from ui.info import MessageWidget


class Debug:
    _parent = None

    @staticmethod
    def init(parent):
        Debug._parent = parent

    @staticmethod
    def _show(message: str, level: str):
        if not Debug._parent:
            print(f"[{level.upper()}] {message}")
            return

        toast = MessageWidget(Debug._parent, message, level)
        toast.show_animated()

    @staticmethod
    def Error(message: str):
        Debug._show(message, "error")

    @staticmethod
    def Warn(message: str):
        Debug._show(message, "warn")

    @staticmethod
    def Log(message: str):
        Debug._show(message, "info")
