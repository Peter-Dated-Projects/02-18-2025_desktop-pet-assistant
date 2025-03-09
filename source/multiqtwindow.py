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

        # create a framebuffer object
        t_image = qtg.QImage(
            constants.WINDOW_SIZE[0],
            constants.WINDOW_SIZE[1],
            qtg.QImage.Format_ARGB32_Premultiplied,
        )
        t_image.fill(qtg.QColor(0, 0, 0, 0))
        self._framebuffer = qtg.QPixmap.fromImage(t_image)

        # create a painter for framebuffer
        self._fb_painter = qtg.QPainter(self._framebuffer)
        self._fb_painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceOver)
        self._fb_painter.setRenderHint(qtg.QPainter.Antialiasing, False)
        self._fb_painter.end()

        # create rect for movement
        self._window_rect = pygame.Rect(
            0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]
        )
        self._fb_rect = qtc.QRectF(
            0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]
        )
        self.initUI()

        # show self
        self.show()

    def initUI(self):
        self.setGeometry(0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1])
        self.setWindowTitle(self._name)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def widget_update(self):
        physics.entity.Entity.update_entity(self)

        print(self.geometry())

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
