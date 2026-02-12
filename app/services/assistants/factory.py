from app.schemas.enums import ProviderType
from app.services.assistants.base import AssistantClient
from app.services.assistants.google_genai import GoogleGenaiClient
from app.services.assistants.ollama import OllamaClient


def get_assistant(provider: str) -> AssistantClient:
    providers = {
        ProviderType.OLLAMA.value: OllamaClient,
        ProviderType.GOOGLE.value: GoogleGenaiClient,
    }

    if provider not in providers:
        raise ValueError(f"Assistant '{provider}' not supported")

    return providers[provider]()
