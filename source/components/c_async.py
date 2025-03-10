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
    # Internal Done Callback Wrapper
    # -------------------------------------------------------- #
    def _done_callback_wrapper(
        self, signal_object, user_callback, callback_args, callback_kwargs, future
    ):
        try:
            # Retrieve the result of the task.
            result = future.result()
            # Call the user callback with the result and any extra callback arguments.
            user_callback(result, *callback_args, **callback_kwargs)
            # Emit the signal with the result.
            signal_object.emit(result)
        except Exception as e:
            # If an error occurred, you can pass None and/or the error.
            user_callback(None, error=e, *callback_args, **callback_kwargs)
            # Optionally, emit the signal with the exception (or handle it as needed).
            signal_object.emit(e)

    # -------------------------------------------------------- #
    # Basic Finished Task Signal (existing approach)
    # -------------------------------------------------------- #
    @staticmethod
    def finished_task_signal(future, signal_object):
        # Simple version that just emits the result.
        signal_object.emit(future.result())

    # -------------------------------------------------------- #
    # Add Task with User Callback Support
    # -------------------------------------------------------- #
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
        # Keep track of the task (for bookkeeping if needed)
        self._tasks.append(task)

        # Retrieve the signal object from your signal handler using the signal name.
        signal_object = constants.SIGNAL_HANDLER.get_signal(signal_name)

        # Ensure defaults for the argument lists/dicts.
        task_args = task_args if task_args is not None else []
        task_kwargs = task_kwargs if task_kwargs is not None else {}
        callback_args = callback_args if callback_args is not None else []
        callback_kwargs = callback_kwargs if callback_kwargs is not None else {}

        # Submit the task to the thread pool.
        future = self._thread_pool.submit(task, *task_args, **task_kwargs)

        # Attach the done callback to the future, binding the extra parameters.
        future.add_done_callback(
            partial(
                self._done_callback_wrapper,
                signal_object,
                user_callback,
                callback_args,
                callback_kwargs,
            )
        )

    # Optionally, you can still support the original add_task method:
    def add_task(self, task: Callable, signal_name: str, args: list = None):
        self._tasks.append(task)
        _f_signal = constants.SIGNAL_HANDLER.get_signal(signal_name)
        future = self._thread_pool.submit(task, *args if args else [])
        future.add_done_callback(
            partial(self.finished_task_signal, signal_object=_f_signal)
        )


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
