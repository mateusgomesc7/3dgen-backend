from sqlalchemy.orm import Session

from app.models.assistant import Assistant
from app.schemas.assistant import AssistantCreate, AssistantUpdate

class AssistantService:
    def __init__(self, session: Session):
        self._db = session
    
    def create_assistant(self, data: AssistantCreate) -> Assistant:
        assistant = Assistant(**data.dict())
        self._db.add(assistant)
        self._db.commit()
        self._db.refresh(assistant)
        return assistant

    def get_assistant(self, assistant_id: int) -> Assistant | None:
        return self._db.query(Assistant).filter(Assistant.id == assistant_id).first()

    def list_assistants(self):
        return self._db.query(Assistant).order_by(Assistant.id.desc()).all()

    def update_assistant(self, assistant: Assistant, data: AssistantUpdate) -> Assistant:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(assistant, field, value)

        self._db.commit()
        self._db.refresh(assistant)
        return assistant

    def delete_assistant(self, assistant: Assistant):
        self._db.delete(assistant)
        self._db.commit()