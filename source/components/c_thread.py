import threading

from source.components import c_component

from typing import Callable

# -------------------------------------------------------- #
# thread component
# -------------------------------------------------------- #


class ThreadComponent(c_component.Component):
    def __init__(self, target: Callable, args=None, kwargs=None):
        super().__init__()
        self._target = target
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self._thread = None
        self._running = False

    def start(self):
        if not self._running:
            self._thread = threading.Thread(
                target=self._target, args=self._args, kwargs=self._kwargs, daemon=True
            )
            self._thread.start()
            self._running = True

    def stop(self):
        if self._running:
            self._thread.join()
            self._running = False
