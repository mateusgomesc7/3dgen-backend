import requests

class OllamaClient:
    def __init__(self, base_url: str = "http://host.docker.internal:11434"):
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
