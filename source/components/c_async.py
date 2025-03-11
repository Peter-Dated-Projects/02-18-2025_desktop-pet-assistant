import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from functools import partial

from source import constants
from source.components import c_component

# ============================================================ #
# Async Operations Manager
# ============================================================ #


class AsyncOperationsHandler:
    def __init__(self):
        # You can optionally specify max_workers here.
        self._thread_pool = ThreadPoolExecutor(max_workers=2)
        self._tasks = []

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    @staticmethod
    def finished_task_signal(future, signal_object, *args):
        # Simple version that just emits the result.
        _args = [future.result()] if future.result() else []
        print("submitting args", _args)
        signal_object.emit(*_args)

    def add_task_with_callback(
        self,
        task: Callable,
        signal_name: str,
        user_callback: Callable = None,
        args: list = None,
    ):
        _args = args if args else []
        _callback = user_callback if user_callback else self.finished_task_signal

        self._tasks.append(task)
        signal_object = constants.SIGNAL_HANDLER.get_signal(signal_name)
        future = self._thread_pool.submit(task, *_args)

        # Attach the done callback to the future, binding the extra parameters.
        future.add_done_callback(partial(_callback, signal_object=signal_object))

    # Optionally, you can still support the original add_task method:
    def add_task(self, task: Callable, signal_name: str, *args):
        self.add_task_with_callback(task, signal_name, None, *args)


# ============================================================ #
# Async Operations Component
# ============================================================ #


class AsyncOperationsComponent(c_component.Component):
    def __init__(self):
        super().__init__()
        self._has_task = False

    # -------------------------------------------------------- #
    # Logic: Delegate task adding to the async handler.
    # -------------------------------------------------------- #
    def add_task(self, task: Callable, signal_name: str, args: list = None):
        constants.ASYNC_TASK_HANDLER.add_task(task, signal_name, args)

    def add_task_with_callback(
        self,
        task: Callable,
        signal_name: str,
        user_callback: Callable,
        task_args: list = None,
        task_kwargs: dict = None,
        callback_args: list = None,
        callback_kwargs: dict = None,
    ):
        constants.ASYNC_TASK_HANDLER.add_task_with_callback(
            task,
            signal_name,
            user_callback,
            task_args,
            task_kwargs,
            callback_args,
            callback_kwargs,
        )
