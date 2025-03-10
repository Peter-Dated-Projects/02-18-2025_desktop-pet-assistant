import asyncio
from ollama import chat
from ollama import ChatResponse
from ollama import AsyncClient

from source import constants

from source.components import c_component

# ============================================================ #
# Ollama API Component
# ============================================================ #

OLLAMA_MODEL = "llama3.2:3b"


class OllamaAPIComponent(c_component.Component):
    def __init__(self, _async: bool = True):
        super().__init__()

        self._async = _async

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        pass

    async def async_chat(self, message: str):
        _packet = {
            "role": "user",
            "content": message,
        }
        async for part in await AsyncClient().chat(
            model=OLLAMA_MODEL,
            messages=[_packet],
            stream=True,
        ):
            yield part["message"]["content"]
