import os
import requests
from dotenv import load_dotenv

from app.services.assistants.base import AssistantClient

load_dotenv()

BASE_URL_OLLAMA = os.getenv("BASE_URL_OLLAMA")
if BASE_URL_OLLAMA is None:
    raise ValueError("BASE_URL_OLLAMA environment variable is not set")

class OllamaClient(AssistantClient):
    def __init__(self, base_url: str = BASE_URL_OLLAMA):
        self.base_url = base_url


    def generate(self, prompt: str, model_name: str) -> str:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "think": False
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=480
        )

        response.raise_for_status()
        return response.json()["response"]


    def list_models(self) -> list:
        response = requests.get(
            f"{self.base_url}/api/tags",
            timeout=10
        )

        response.raise_for_status()
        return response.json().get("models", [])
