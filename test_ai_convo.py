import requests
import json
import os
import time
import random
from typing import List, Dict


import ollama


class OllamaChat:
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
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
        self._description = self.chat(
            "Admin Query: provide a description of yourself. Be sure to include (point form required): [name, age, sex, hobbies, interests, and physical description]"
        )

    def _send_request(self, prompt: str, stream: bool = False) -> Dict:
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
            messages = self.context + messages

        data = {"model": self.model, "messages": messages, "stream": stream}

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()

    def chat(self, prompt: str) -> str:
        """
        Send a message to the chat and get the response

        Args:
            prompt: The user's input message

        Returns:
            The assistant's response
        """
        try:
            response = self._send_request(prompt)

            # Update context with both user message and assistant response
            self.context.append({"role": "user", "content": prompt})
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

            return response["message"]["content"]

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


def main():
    print("Ollama Chat Client - Type 'exit' to quit or 'save' to save session")

    # Initialize chat
    chats = [OllamaChat(model="a_Celia"), OllamaChat(model="a_Elaina")]

    # Try to load previous session
    for c in chats:
        if c.load_session():
            print(f"\nPrevious session loaded for {c.model} successfully.")

        # output descriptoin
        print(f"\n{c.model}: {c._description}")
        print("=" * 100)

    # ------------------------------------------------------------------ #
    # setup convo
    # ------------------------------------------------------------------ #

    print("=" * 100)
    print("Setting up conversation...")
    print("=" * 100)

    # setup for conversation
    conversation_start_prompt = (
        "this is a meet and greet between my two assistants, Elaina and Byte. "
        "Elaina is a wise and knowledgeable assistant, while Byte is a fun and playful assistant. "
        "Peter is not present in this conversation. "
        "The assistants should introduce themselves and start a conversation. "
    )
    print("Prompt:", conversation_start_prompt)

    # start by sharing the description of the assistants
    _descriptions = "Descriptions of conversation participants:\n" + "\n\n".join(
        [c._description for c in chats]
    )
    print("=" * 100)

    for c in chats:
        _descriptions_response = c.chat(conversation_start_prompt + _descriptions)
        print(f"\n{c.model}: {_descriptions_response}")
        print("\n\n")
        print("=" * 100)

    active_user_ind = random.randint(0, 1)
    _opposite_response = chats[active_user_ind].chat(
        f"{chats[active_user_ind].model}: Hello! How are you?"
    )

    print(f"\n{chats[active_user_ind].model}: Hello! How are you?")
    print(f"\n{chats[active_user_ind].model}: {_opposite_response}")

    # run input loop
    while True:
        try:
            active_user_ind = (active_user_ind + 1) % len(chats)

            _opposite_response = chats[active_user_ind].chat(_opposite_response)
            print("=" * 100)
            print(f"\n{chats[active_user_ind].model}: {_opposite_response}")

            time.sleep(1)
            # create a topic for the conversation

            # if user_input.lower() == 'exit':
            #     # Save before exiting
            #     chat1.save_session()
            #     print("Chat session saved. Goodbye!")
            #     break

            # elif user_input.lower() == 'save':
            #     chat1.save_session()
            #     print("Chat session saved.")
            #     continue

            # response = chat1.chat(user_input)

        except KeyboardInterrupt:
            for c in chats:
                c.save_session()
            print("\nChat session saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
