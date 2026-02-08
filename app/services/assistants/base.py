from abc import ABC, abstractmethod

class AssistantClient(ABC):

    @abstractmethod
    def generate(self, content: str, history: list[dict], model_name: str) -> str:
        pass

    @abstractmethod
    def build_message_dict(self, role: str, content: str) -> dict:
        pass

    @abstractmethod
    def list_models(self) -> list:
        pass
