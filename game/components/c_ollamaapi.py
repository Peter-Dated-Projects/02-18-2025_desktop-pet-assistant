import os
import uuid
import json
import ollama
import requests

from source import constants
from source.components import c_component

from typing import Callable, List, Dict, Any

# ============================================================ #
# ollama api handler class
# ============================================================ #


class OllamaChat:
    def __init__(
        self, model: str = "llama3.2", base_url: str = "http://localhost:11434"
    ):
        """
        Initialize the chat with a specific model and Ollama server URL

        Args:
            model: The model to use (e.g., "llama2", "mistral", etc.)
            base_url: URL of your Ollama server (default: localhost)
        """
        self.model = model
        self.base_url = base_url
        self.context = []
        self.session_history: List[Dict] = []

        self._client = ollama.Client(host=base_url)

    def _send_request(
        self, prompt: str, stream: bool = False, with_context: bool = True
    ) -> Dict:
        """
        Send a request to the Ollama API and return the response
        Args:
            prompt: The user's input message
            stream: Whether to stream the response (default: False)
        Returns:
            The response from the Ollama API
        Raises:
            requests.exceptions.RequestException: If the request fails
        """

        url = f"{self.base_url}/api/chat"
        headers = {"Content-Type": "application/json"}

        # Prepare the messages including previous context
        messages = [{"role": "user", "content": prompt}]
        if self.context:
            messages = self.context if with_context else [] + messages

        data = {"model": self.model, "messages": messages, "stream": stream}

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()

    def chat(
        self, prompt: str, speaker: str = "user", with_context: bool = True
    ) -> str:
        """
        Send a message to the chat and get the response

        Args:
            prompt: The user's input message

        Returns:
            The assistant's response
        """
        try:
            response = self._send_request(prompt, with_context=with_context)

            # Update context with both user message and assistant response
            self.context.append({"role": speaker, "content": prompt})
            self.context.append(
                {"role": "assistant", "content": response["message"]["content"]}
            )

            # Keep only the last N messages to manage context length
            max_context = 10  # Adjust based on your needs
            if len(self.context) > max_context * 2:
                self.context = self.context[-max_context * 2 :]

            # Save to session history
            self.session_history.append(
                {"user": prompt, "assistant": response["message"]["content"]}
            )

            return response

        except requests.exceptions.RequestException as e:
            return f"Error communicating with Ollama API: {str(e)}"

    def save_session(self, folder_path: str = "chats"):
        """Save the current chat session to a file"""
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{self.model}.json")
        with open(file_path, "w") as f:
            json.dump(
                {
                    "model": self.model,
                    "context": self.context,
                    "history": self.session_history,
                },
                f,
                indent=2,
            )

    def load_session(self, folder_path: str = "chats") -> bool:
        """Load a chat session from a file"""
        file_path = os.path.join(folder_path, f"{self.model}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                self.model = data.get("model", self.model)
                self.context = data.get("context", [])
                self.session_history = data.get("history", [])
            return True
        return False


# ============================================================ #
# Ollama API Component
# ============================================================ #

OLLAMA_MODEL = "llama3.2"


class OllamaAPIComponent(c_component.Component):
    @classmethod
    def generate_unique_signal_name(cls):
        return f"ollamaapi_{uuid.uuid4()}"

    def __init__(
        self, _async: bool = True, callback_func: Callable = None, model: str = None
    ):
        super().__init__()
        self._signal_name = self.generate_unique_signal_name()
        self._async = _async

        constants.SIGNAL_HANDLER.register_signal(self._signal_name, [Any, Any])
        self._receiver = constants.SIGNAL_HANDLER.register_receiver(
            self._signal_name, self.receive_signal
        )

        self._client = OllamaChat(
            model=model if model is not None else OLLAMA_MODEL,
        )
        self._client.load_session()

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        pass

    def receive_signal(self, ollama_client, result):
        print("finished query", ollama_client, result)

        print("\n\n")
        print(result["message"])
        print("\n\n")
        self._client.save_session()

    @staticmethod
    def finished_task_signal(future, signal_object, _args):
        result = future.result() if future.result() else []
        print("submitting args", result, "\nInputted args", _args)
        signal_object.emit(_args[0], result)

    def query_ollama(
        self, prompt: str, with_context: bool = True, _callback_func: Callable = None
    ) -> str:
        """Query the Ollama API and get a response."""
        constants.ASYNC_TASK_HANDLER.add_task_with_callback(
            _default_query,
            self._signal_name,
            user_callback=self.finished_task_signal,
            args=[self._client, prompt, with_context],
        )


def _default_query(ollama_client, prompt, with_context):
    """Default query function for the Ollama API."""
    print("sending query: ", prompt)
    return ollama_client.chat(prompt, speaker="user", with_context=with_context)
