import pygame
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from source import constants
from source import physics

from source import multiqtwindow

# -------------------------------------------------------- #
# window wrapper
# -------------------------------------------------------- #


class HiddenWindowWrapper(multiqtwindow.WindowWrapper):
    def __init__(self, name: str, area: pygame.Rect):
        super().__init__(name, area)

        # create a painter for framebuffer
        self._fb_painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceOver)
        self._fb_painter.setRenderHint(qtg.QPainter.Antialiasing, False)

    def initUI(self):
        super().initUI()
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def widget_update(self):
        physics.entity.Entity.update_entity(self)

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
        super().paintEvent(event)
