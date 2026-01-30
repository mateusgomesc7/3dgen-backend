from datetime import datetime
from sqlalchemy.orm import Session

from app.ollama.ollama_client import OllamaClient
from app.models.assistant import Assistant
from app.schemas.assistant import AssistantCreate, AssistantUpdate

class AssistantService:
    def __init__(self, session: Session):
        self._db = session
        self._ollama = OllamaClient()
    
    def create_assistant(self, data: AssistantCreate) -> Assistant:
        assistant = Assistant(**data.dict())
        self._db.add(assistant)
        self._db.commit()
        self._db.refresh(assistant)
        return assistant

    def get_assistant(self, assistant_id: int) -> Assistant | None:
        return self._db.query(Assistant).filter(Assistant.id == assistant_id).first()

    def list_assistants(self, is_active: bool | None = None) -> list[Assistant]:
        query = self._db.query(Assistant).order_by(Assistant.id.desc())
        if is_active is not None:
            query = query.filter(Assistant.is_active == is_active)
        return query.all()

    def update_assistant(self, assistant: Assistant, data: AssistantUpdate) -> Assistant:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(assistant, field, value)

        self._db.commit()
        self._db.refresh(assistant)
        return assistant

    def delete_assistant(self, assistant: Assistant):
        self._db.delete(assistant)
        self._db.commit()
    
    def sync_models(self):
        models_ollama = self._ollama.list_models()
        ollama_model_names = {m["name"] for m in models_ollama}

        all_assistants = self._db.query(Assistant).all()
        existing_assistants_dict = {a.name: a for a in all_assistants}

        for name, assistant in existing_assistants_dict.items():
            if name in ollama_model_names:
                assistant.is_active = True
                assistant.last_checked_at = datetime.now()
            else:
                assistant.is_active = False

        new_count = 0
        for model_name in ollama_model_names:
            if model_name not in existing_assistants_dict:
                new_assistant = Assistant(
                    name=model_name, 
                    is_active=True,
                    last_checked_at=datetime.now()
                )
                self._db.add(new_assistant)
                new_count += 1

        self._db.commit()
        return f"Synchronization complete. {new_count} new models added."
    