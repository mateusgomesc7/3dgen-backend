import os
from google import genai
from dotenv import load_dotenv

from app.services.assistants.base import AssistantClient

load_dotenv()


API_KEY_GOOGLE_GENAI = os.getenv("API_KEY_GOOGLE_GENAI")
if API_KEY_GOOGLE_GENAI is None:
    raise ValueError("API_KEY_GOOGLE_GENAI environment variable is not set")

class GoogleGenaiClient(AssistantClient):
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY_GOOGLE_GENAI)


    def generate(self, prompt: str, model_name: str) -> str:
        response = self.client.models.generate_content(
            model=model_name, contents=[prompt]
        )
        return response.text or ""


    def list_models(self) -> list:
        try:
            models_list = []
            exclude_keywords = [
                "-image", "image-preview", "image-generation", 
                "tts", "robotics", "computer-use", "research"
            ]

            for m in self.client.models.list(): # Only max 50 models are returned
                if not m.name:
                    continue
                    
                name_lower = m.name.lower()

                can_generate = m.supported_actions and "generateContent" in m.supported_actions
                is_specialized = any(keyword in name_lower for keyword in exclude_keywords)

                if can_generate and not is_specialized:
                    models_list.append({
                        "name": m.name,
                        "display_name": m.display_name,
                        "description": m.description
                    })
            return models_list
        except Exception as e:
            print(f"Error listing Google GenAI models: {e}")
            return []
