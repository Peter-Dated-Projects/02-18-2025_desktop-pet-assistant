import pygame
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from source import constants
from source import physics


# -------------------------------------------------------- #
# window wrapper
# -------------------------------------------------------- #


class WindowWrapper(physics.entity.Entity, qtw.QWidget):
    def __init__(self, name: str, area: pygame.Rect):
        physics.entity.Entity.__init__(self, 0, 0, area.width, area.height)
        qtw.QWidget.__init__(self)
        self._name = name

        # layout
        self._layout = qtw.QVBoxLayout()

        # create a framebuffer object
        t_image = qtg.QImage(
            area.width,
            area.height,
            qtg.QImage.Format_ARGB32_Premultiplied,
        )
        t_image.fill(qtg.QColor(0, 0, 0, 0))
        self._framebuffer = qtg.QPixmap.fromImage(t_image)

        # create a painter for framebuffer
        self._fb_painter = qtg.QPainter(self._framebuffer)

        # create rect for movement
        self._window_rect = pygame.Rect(0, 0, area.width, area.height)
        self._fb_rect = qtc.QRectF(0, 0, area.width, area.height)
        self.initUI()

        # show self
        self.show()

    def initUI(self):
        self.setGeometry(0, 0, self._window_rect.width, self._window_rect.height)
        self.setWindowTitle(self._name)
        self.setLayout(self._layout)

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def widget_update(self):
        physics.entity.Entity.update_entity(self)

        # print(self.geometry())

    def window_update(self):
        # create framebuffer painter
        self._fb_painter.begin(self._framebuffer)
        self._fb_painter.setRenderHint(qtg.QPainter.Antialiasing, False)
        self._framebuffer.fill(qtg.QColor(0, 0, 0, 0))

        # enter rendering code
        self.widget_update()

        # end of render + finish update
        self._fb_painter.end()
        self.move(self._window_rect.x, self._window_rect.y)
        self.update()

    def paintEvent(self, event):
        # print("painting")
        painter = qtg.QPainter(self)
        painter.drawPixmap(self._fb_rect.topLeft(), self._framebuffer)
