import os

import requests
from dotenv import load_dotenv

from app.services.ai.prompt import THREEJS_SYSTEM_PROMPT
from app.services.assistants.base import AssistantClient

load_dotenv()

BASE_URL_OLLAMA = os.getenv('BASE_URL_OLLAMA')
if BASE_URL_OLLAMA is None:
    raise ValueError('BASE_URL_OLLAMA environment variable is not set')


class OllamaClient(AssistantClient):
    def __init__(self, base_url: str = BASE_URL_OLLAMA):
        self.base_url = base_url

    def generate(self, content: str, history: list[dict], model_name: str) -> str:
        messages = self._build_messages(history, content)

        payload = {
            'model': model_name,
            'messages': messages,
            'stream': False,
            'think': False,
        }

        response = requests.post(f'{self.base_url}/api/chat', json=payload, timeout=480)

        response.raise_for_status()
        return response.json()['message']['content']

    def build_message_dict(self, role: str, content: str) -> dict:
        return {'role': role, 'content': content}

    def list_models(self) -> list:
        response = requests.get(f'{self.base_url}/api/tags', timeout=10)

        response.raise_for_status()
        return response.json().get('models', [])

    def _build_messages(self, history: list[dict], content: str) -> list[dict]:
        messages = [self.build_message_dict('system', THREEJS_SYSTEM_PROMPT)]

        messages.extend(history)

        messages.append(self.build_message_dict('user', content))

        return messages
