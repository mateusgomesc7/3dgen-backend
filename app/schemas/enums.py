from enum import Enum

class ProviderType(str, Enum):
    OLLAMA = "ollama"
    GOOGLE = "google"
