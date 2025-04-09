import time
import os
import pyaudio
import pvporcupine
import numpy as np

from source import signal
from source import constants
from source.components import c_thread

from typing import List

# -------------------------------------------------------- #
# wake word component
# -------------------------------------------------------- #


def _async_pause(pause_time: float):
    """
    This function is used to pause the thread for a given amount of time.
    :param pause_time: The amount of time to pause the thread for.
    """
    print("Pausing for", pause_time, "seconds")
    time.sleep(pause_time)


class WakeWordComponent(c_thread.ThreadComponent):

    def __init__(
        self,
        keywords_path: List[str],
        keywords: List[str],
        _callback_event_name: str,
        weights: List[float],
        pause_time: float = 1,
    ):
        super().__init__(self._run)
        self._keywords = keywords
        self._keywords_path = keywords_path

        self._porcupine = None
        self._audio_stream = None
        self._callback_event_name = _callback_event_name
        self._pause_time = pause_time
        self._paused = False

        self._callback_signal = constants.SIGNAL_HANDLER.get_signal(
            self._callback_event_name
        )

        # create audio stream and porcupine instance
        _pyaudio = pyaudio.PyAudio()
        _porcupine = pvporcupine.create(
            access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
            keywords=keywords,
            keyword_paths=self._keywords_path,
            sensitivities=(
                weights
                if weights
                else [0.5] * (len(self._keywords_path) + len(self._keywords))
            ),
        )

        # create the audio stream + porcupine instance
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
            if result >= 0 and not self._paused:
                _result = (
                    self._keywords[result]
                    if self._keywords
                    else self._keywords_path[result]
                )
                self._callback_signal.emit(_result)
                self._paused = True
                # emit a signal to activate an async callback
                constants.ASYNC_TASK_HANDLER.add_task_with_callback(
                    _async_pause,
                    f"{id(self)}_wake_word_callback",
                    self._async_callback,
                    args=[self._pause_time],
                )

    def _async_callback(self, future, signal_object, *args):
        """
        This callback means the wake word was detected and designated pause time has
        passed. It will stop the wake word detection and restart it.
        """

        print(future, signal_object, args)
        print("Starting audio detection again")
        self._paused = False
