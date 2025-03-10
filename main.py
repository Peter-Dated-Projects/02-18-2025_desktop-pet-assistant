import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import sys
import time
import pygame
import os

from source import constants
from source import physics

from source.components import c_async

# -------------------------------------------------------- #
# Desktop Pet Assistant
# -------------------------------------------------------- #

from source import world
from source import signal

from game import assistant

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# -------------------------------------------------------- #
# main application
# -------------------------------------------------------- #


class DesktopPetAssistantApplication:
    def __init__(self):
        constants.APP_CONTEXT = self
        constants.SIGNAL_HANDLER = signal.SignalHandler()
        constants.ASYNC_TASK_HANDLER = c_async.AsyncOperationsHandler()

        self.app = qtw.QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)

        # store all active windows
        self._world = world.World()

        # -------------------------------------------------------- #
        # game loop

        self._timer = qtc.QTimer()
        self._timer.timeout.connect(self.game_loop)
        self._timer.start(1000 // constants.FPS)
        constants.END_TIME = time.time()

        # -------------------------------------------------------- #
        # graphics startup

        # output logging into
        screen_size = self._world._visible_world_rect
        print(f"Screen: {screen_size[2]}x{screen_size[3]}")
        print(f"Screen topleft: {self._world._visible_world_rect.topleft}")

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    # -------------------------------------------------------- #
    # pyqt logic
    # -------------------------------------------------------- #

    def game_loop(self):
        if not constants.RUNNING:
            self.app.quit()
            return

        # update delta time variables
        constants.START_TIME = time.time()
        constants.DELTA_TIME = constants.START_TIME - constants.END_TIME
        constants.END_TIME = constants.START_TIME
        constants.RUNTIME += constants.DELTA_TIME

        # update world
        self._world.update()

        print("\n")

    def run(self):
        sys.exit(self.app.exec_())


# -------------------------------------------------------- #
# main
# -------------------------------------------------------- #

if __name__ == "__main__":
    application = DesktopPetAssistantApplication()

    # add entities
    application._world.add_entity(assistant.Assistant("test"))
    application._world.add_entity(assistant.Assistant("stella.ai"))

    application.run()
