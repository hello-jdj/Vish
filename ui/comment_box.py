from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF
from PySide6.QtGui import QPen, QColor


class CommentBoxItem(QGraphicsRectItem):
    def __init__(self, rect=QRectF(0, 0, 300, 200), title="Comment"):
        super().__init__(rect)

        self.setFlags(
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemIsSelectable
        )

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable)
        self.setZValue(-10)

        self.resize_margin = 10
        self.resizing = False
        self.resize_corner = None

        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(2)
        self.setPen(pen)
        self.setBrush(QColor(255, 255, 255, 40))

        self.title_item = QGraphicsTextItem(title, self)
        self.title_item.setDefaultTextColor(QColor(240, 240, 240))

        self.title_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.title_item.setFlag(QGraphicsTextItem.ItemIsFocusable)

        self.title_padding = 8
        self._update_title_position()

    def _update_title_position(self):
        r = self.rect()
        max_width = r.width() - self.title_padding * 2
        self.title_item.setTextWidth(max(50, max_width))
        self.title_item.document().adjustSize()
        self.title_item.setPos(
            self.title_padding,
            self.title_padding
        )


    def _get_resize_corner(self, pos: QPointF):
        r = self.rect()
        m = self.resize_margin

        if QRectF(r.topLeft(), QSizeF(m, m)).contains(pos):
            return "tl"
        if QRectF(r.topRight() - QPointF(m, 0), QSizeF(m, m)).contains(pos):
            return "tr"
        if QRectF(r.bottomLeft() - QPointF(0, m), QSizeF(m, m)).contains(pos):
            return "bl"
        if QRectF(r.bottomRight() - QPointF(m, m), QSizeF(m, m)).contains(pos):
            return "br"
        return None

    def hoverMoveEvent(self, event):
        corner = self._get_resize_corner(event.pos())
        if corner:
            match corner:
                case "tl":
                    self.setCursor(Qt.SizeFDiagCursor)
                case "tr":
                    self.setCursor(Qt.SizeBDiagCursor)
                case "bl":
                    self.setCursor(Qt.SizeBDiagCursor)
                case "br":
                    self.setCursor(Qt.SizeFDiagCursor)
                case _:
                    self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if self.title_item.isUnderMouse():
            event.ignore()
            return
        self.resize_corner = self._get_resize_corner(event.pos())
        self.resizing = self.resize_corner is not None
        self.drag_start_pos = event.pos()
        self.original_rect = QRectF(self.rect())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.resizing:
            super().mouseMoveEvent(event)
            return

        delta = event.pos() - self.drag_start_pos
        r = QRectF(self.original_rect)

        if self.resize_corner == "br":
            r.setBottomRight(r.bottomRight() + delta)
        elif self.resize_corner == "bl":
            r.setBottomLeft(r.bottomLeft() + delta)
        elif self.resize_corner == "tr":
            r.setTopRight(r.topRight() + delta)
        elif self.resize_corner == "tl":
            r.setTopLeft(r.topLeft() + delta)

        self.setRect(r.normalized())
        self._update_title_position()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.resize_corner = None
        super().mouseReleaseEvent(event)

    def setRect(self, rect: QRectF):
        super().setRect(rect)
        self._update_title_position()

