from abc import ABC, abstractmethod

class AssistantClient(ABC):

    @abstractmethod
    def generate(self, prompt: str, model_name: str) -> str:
        pass


    @abstractmethod
    def list_models(self) -> list:
        pass
