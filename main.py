import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import sys
import time
import pygame
import os

from source import constants

# ======================================================== #
# Desktop Pet Assistant
# ======================================================== #

from source import world
from source import signal

from game import assistant

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class DesktopPetAssistant(qtw.QMainWindow):
    def __init__(self):
        self.app = qtw.QApplication(
            sys.argv
        )  # Create the QApplication before any widgets
        super().__init__()

        # -------------------------------------------------------- #
        # internal logic
        # -------------------------------------------------------- #

        constants.WINDOW_CONTEXT = self
        constants.SIGNAL_HANDLER = signal.SignalHandler()

        self._world = world.World()
        self.initUI()

        # TODO - remove debug canvas
        self.setAttribute(qtc.Qt.WA_NoSystemBackground, True)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground, True)
        t_image = qtg.QImage(
            constants.WINDOW_SIZE[0],
            constants.WINDOW_SIZE[1],
            qtg.QImage.Format_ARGB32_Premultiplied,
        )
        t_image.fill(qtg.QColor(0, 0, 0, 0))
        self._framebuffer = qtg.QPixmap.fromImage(t_image)

        self._fb_painter = qtg.QPainter(self._framebuffer)
        self._fb_painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceOver)
        self._fb_painter.setRenderHint(qtg.QPainter.Antialiasing, False)
        self._fb_painter.end()

        self._rect = pygame.Rect(
            0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]
        )
        # -------------------------------------------------------- #
        # game loop
        # -------------------------------------------------------- #

        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000 // constants.FPS)
        constants.END_TIME = time.time()

        # -------------------------------------------------------- #
        # game objects
        # -------------------------------------------------------- #

        self._world.add_entity(assistant.Assistant())

    def initUI(self):
        # check if mac or not
        # if sys.platform != "darwin":
        #     print("Mac version not running on a mac? (or linux)")
        #     sys.exit()

        # create a pyqt5 app that fills the entire visible screen with a transparent background
        screen_size = self._world._visible_world_rect
        print(f"Screen: {screen_size[2]}x{screen_size[3]}")
        print(f"Screen topleft: {self._world._visible_world_rect.topleft}")

        self.setGeometry(0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1])

        # window params
        self.setWindowTitle("Hello World")
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:rgba(0, 0, 0, 0);")
        self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)
        self.show()

        # Install event filter
        self.app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in (
            qtc.QEvent.MouseButtonPress,
            qtc.QEvent.MouseButtonRelease,
            qtc.QEvent.MouseMove,
        ):
            if not self._rect.collidepoint((event.pos().x(), event.pos().y())):
                return False  # Pass through the event
        # print(event)
        return super().eventFilter(obj, event)

    def game_loop(self):
        if not constants.RUNNING:
            self.app.quit()
            return

        constants.START_TIME = time.time()
        constants.DELTA_TIME = constants.START_TIME - constants.END_TIME
        constants.END_TIME = constants.START_TIME
        constants.RUNTIME += constants.DELTA_TIME

        # create framebuffer painter
        self._fb_painter.begin(self._framebuffer)
        self._fb_painter.setRenderHint(qtg.QPainter.Antialiasing, False)
        self._framebuffer.fill(qtg.QColor(0, 0, 0, 0))

        # Update the world with the delta time
        self._world.update()

        # end of render
        self._fb_painter.end()

        # update geometry
        self.setGeometry(
            self._rect.x,
            self._rect.y,
            self._rect.width,
            self._rect.height,
        )

        self.update()

    def paintEvent(self, event):
        painter = qtg.QPainter(self)
        painter.setRenderHint(qtg.QPainter.Antialiasing, False)
        painter.drawPixmap(0, 0, self._framebuffer)

    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == qtc.Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
            self._rect.topleft = (new_pos.x(), new_pos.y())
            event.accept()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    assistant = DesktopPetAssistant()
    assistant.run()
