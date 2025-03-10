import uuid
import asyncio
from ollama import chat
from ollama import ChatResponse
from ollama import AsyncClient

from source import constants

from source.components import c_component

from typing import Callable, List

# ============================================================ #
# Ollama API Component
# ============================================================ #

OLLAMA_MODEL = "llama3.2:3b"


def _default_callback():
    pass


class OllamaAPIComponent(c_component.Component):
    @classmethod
    def generate_unique_signal_name(cls):
        return f"ollamaapi_{uuid.uuid4()}"
    
    def __init__(self, _async: bool = True, callback_func: Callable = None):
        super().__init__()
        self._signal_name = self.generate_unique_signal_name()
        self._async = _async
        
        constants.SIGNAL_HANDLER.register_signal(self._signal_name, [str])
        self._receiver = constants.SIGNAL_HANDLER.register_receiver(
            self._signal_name, self.run_task
        )

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        pass

    def run_task(self, prompt: str, callback_func: Callable):
        pass
