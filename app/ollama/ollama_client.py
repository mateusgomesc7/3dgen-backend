import os
import requests
from app.ollama.prompts import THREEJS_SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

BASE_URL_OLLAMA = os.getenv("BASE_URL_OLLAMA")
if BASE_URL_OLLAMA is None:
    raise ValueError("BASE_URL_OLLAMA environment variable is not set")

class OllamaClient:
    def __init__(self, base_url: str = BASE_URL_OLLAMA):
        self.base_url = base_url


    def generate(self, prompt: str) -> str:
        payload = {
            "model": "gemma3:latest",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        return response.json()["response"]


    def generate_threejs(self, user_prompt: str, model_name: str) -> str:
        final_prompt = f"""
            {THREEJS_SYSTEM_PROMPT}

            USER REQUEST:
            {user_prompt}
        """

        payload = {
            "model": model_name,
            "prompt": final_prompt,
            "stream": False
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=90
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
