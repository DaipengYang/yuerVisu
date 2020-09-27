from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSize

class Canvas(QWidget):
    def __init__(self):
        super(Canvas, self).__init__()
        self._painter = QPainter()
        self.pixmap = None  # self.pixmap = QPixmap(), this will throw error
        self.pixmap_size = None
        self.zoom_rate = 100

    def paintEvent(self, QPaintEvent):
        if self.pixmap is None:
            return super(Canvas, self).paintEvent(QPaintEvent)
        painter = self._painter
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        showed_pixmap_size = self.get_showed_size(self.pixmap_size)
        showed_pixmap = self.pixmap.scaled(showed_pixmap_size)
        self.setMinimumSize(showed_pixmap_size)
        painter.drawPixmap(0, 0, showed_pixmap)
        painter.end()

    def get_showed_size(self, pixmap_size):
        height = pixmap_size.height()
        width = pixmap_size.width()
        showed_height = int(height*self.zoom_rate/100)
        showed_width = int(width*self.zoom_rate/100)
        return QSize(showed_width, showed_height)

    def load_pixmap(self, pixmap):
        self.pixmap = pixmap
        if self.pixmap is None:
            return
        self.pixmap_size = self.pixmap.size()
        self.repaint()