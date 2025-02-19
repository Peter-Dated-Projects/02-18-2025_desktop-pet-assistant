import PyQt5
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import os
import sys
import time

from source import constants

# ======================================================== #
# Desktop Pet Assistant
# ======================================================== #

from source import world
from source import screen


class DesktopPetAssistant(qtw.QMainWindow):
    def __init__(self):
        self.app = qtw.QApplication(
            sys.argv
        )  # Create the QApplication before any widgets
        super().__init__()

        # -------------------------------------------------------- #
        # internal logic
        # -------------------------------------------------------- #
        self._world = world.World()
        self.initUI()

        # TODO - remove debug canvas
        self._framebuffer = qtg.QPixmap(
            constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]
        )
        self._framebuffer.fill(qtg.QColor(255, 192, 203))

        # -------------------------------------------------------- #
        # game loop
        # -------------------------------------------------------- #
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000 // constants.FPS)

    def initUI(self):
        # check if mac or not
        if sys.platform != "darwin":
            print("Mac version not running on a mac? (or linux)")
            sys.exit()

        # create a pyqt5 app that fills the entire visible screen with a transparent background
        screen_size = self._world._visible_world_rect
        print(f"Screen: {screen_size[0]}x{screen_size[1]}")
        print(f"Screen topleft: {self._world._visible_world_rect.topleft}")
        self.setGeometry(0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1])

        # window params
        self.setWindowTitle("Hello World")
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:rgba(255, 192, 203, 1.0);")
        self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)
        self.show()

        # Define the region where inputs should be captured
        self.rect = qtc.QRect(100, 100, 300, 300)  # Example region

        # Install event filter
        self.app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in (
            qtc.QEvent.MouseButtonPress,
            qtc.QEvent.MouseButtonRelease,
            qtc.QEvent.MouseMove,
        ):
            if not self.rect.contains(event.pos()):
                return False  # Pass through the event
        # print(event)
        return super().eventFilter(obj, event)

    def game_loop(self):
        constants.START_TIME = time.time()
        constants.DELTA_TIME = constants.START_TIME - constants.END_TIME
        constants.END_TIME = constants.START_TIME

        # Update the world with the delta time
        self._world.update()

    # draw event
    def paintEvent(self, event):
        painter = qtg.QPainter(self)
        painter.drawPixmap(0, 0, self._framebuffer)

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    assistant = DesktopPetAssistant()
    assistant.run()
