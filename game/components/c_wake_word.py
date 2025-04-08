import os
import pyaudio
import pvporcupine
import numpy as np

from source import constants
from source import signal
from source.components import c_thread

from typing import List

# -------------------------------------------------------- #
# wake word component
# -------------------------------------------------------- #


class WakeWordComponent(c_thread.ThreadComponent):

    def __init__(
        self, keywords_path: List[str], keywords: List[str], _callback_event_name: str
    ):
        super().__init__(self._run)
        self._keywords = keywords
        self._keywords_path = keywords_path

        self._porcupine = None
        self._audio_stream = None
        self._callback_event_name = _callback_event_name

        self._callback_signal = constants.SIGNAL_HANDLER.get_signal(
            self._callback_event_name
        )

        # create audio stream and porcupine instance
        _pyaudio = pyaudio.PyAudio()
        _porcupine = pvporcupine.create(
            access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
            keyword_paths=self._keywords_path,
            sensitivities=[0.5] * (len(self._keywords) + len(self._keywords_path)),
        )

        self._audio_stream = _pyaudio.open(
            rate=_porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=_porcupine.frame_length,
        )
        self._porcupine = _porcupine

    def _run(self):
        self._audio_stream = pyaudio.PyAudio().open(
            rate=self._porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self._porcupine.frame_length,
        )

        while self._running:
            pcm = self._audio_stream.read(self._porcupine.frame_length)
            pcm = np.frombuffer(pcm, dtype=np.int16)
            result = self._porcupine.process(pcm)

            if result >= 0:
                _result = f"Keyword {self._keywords[result] if self._keywords else self._keywords_path[result]} detected"
                self._callback_signal.emit(_result)
                print(result)
