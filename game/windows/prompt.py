import pygame
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


from source import constants
from source import multiqtwindow

from game.components import c_wake_word
from game.components import c_ollamaapi

# ============================================================ #
# Prompt class
# ============================================================ #

# This class is used to display a prompt to the user and get their input (text)


class Prompt(multiqtwindow.WindowWrapper):

    def __init__(self, name: str):
        super().__init__(name, pygame.Rect(10, 10, 400, 50))
        self._prompt_text = ""
        self._input_text = ""
        self._is_prompting = False

        # add an input object
        self._input = qtw.QLineEdit(self)
        self._input.setGeometry(0, 0, 400, 50)

        self._layout.addWidget(self._input)
        self._keyword_map = {
            "assets/celia.ppn": self._activate_keyword_callback,
            "assets/bye_celia.ppn": self._deactivate_keyword_callback,
        }

        # ------------------------------------------------------- #
        # components
        # -------------------------------------------------------- #

        self._c_wake_word = self.add_component(
            c_wake_word.WakeWordComponent(
                ["assets/celia.ppn", "assets/bye_celia.ppn"],
                [],
                "voice_activated",
                weights=[0.6, 0.4],
            ),
        )
        self._c_ollama = self.add_component(
            c_ollamaapi.OllamaAPIComponent(model="a_Celia"),
        )
        self._c_wake_word.start()

        constants.SIGNAL_HANDLER.register_receiver(
            "voice_activated", self._keyword_callback
        )
        self.hide()

    def initUI(self):
        super().initUI()
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.setWindowFlags(self.windowFlags() | qtc.Qt.WindowStaysOnTopHint)

    # --------------------------------------------------- #
    # logic
    # --------------------------------------------------- #

    def window_update(self):
        if not self.isVisible():
            return

        # fill background image with red
        self._fb_painter.begin(self._framebuffer)
        # clear
        self._fb_painter.setRenderHint(qtg.QPainter.Antialiasing, False)
        self._framebuffer.fill(qtg.QColor(0, 0, 0, 0))
        # enter rendering code
        self._fb_painter.setCompositionMode(qtg.QPainter.CompositionMode_Source)
        self._fb_painter.fillRect(
            self._fb_rect,
            qtg.QColor(0, 0, 0, 80),
        )

        self._fb_painter.end()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        # when user presses escape and is visible
        if self.isVisible() and event.key() == qtc.Qt.Key_Escape:
            # clear input text
            self._input.clear()
            self._is_prompting = False
            self.hide()
        if self.isVisible() and event.key() == qtc.Qt.Key_Return:
            # get input text
            self._input_text = self._input.text()
            self._is_prompting = False

            # request from ollama
            print(f"Input text: {self._input_text}")
            self._c_ollama.query_ollama(self._input_text)

            # clear input text
            self._input.clear()
            # hide prompt
            self.hide()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self._input.setFocus(qtc.Qt.FocusReason.ActiveWindowFocusReason)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        # if the prompt is not visible, do not set focus
        if not self.isVisible():
            return
        # set focus to input -- hide if no input
        if self._input.text() == "":
            self._is_prompting = False
            self.hide()

            # create an ollama request

        else:
            # set focus to input
            self._input.setFocus(qtc.Qt.FocusReason.ActiveWindowFocusReason)

    # -------------------------------------------------------- #

    def _keyword_callback(self, keyword: str):
        if keyword not in self._keyword_map:
            print(f"Keyword {keyword} not in keyword map")
            return

        print("=" * 20)
        self._keyword_map[keyword](keyword)

    def _activate_keyword_callback(self, keyword: str):
        print(f"Keyword detected: {keyword}")
        self._is_prompting = True
        self.show()

        # make focus
        self.raise_()
        self.activateWindow()
        self._input.setFocus(qtc.Qt.FocusReason.ActiveWindowFocusReason)

    def _deactivate_keyword_callback(self, keyword: str):
        print(f"Keyword detected: {keyword}")
        self._is_prompting = False
        self.hide()
