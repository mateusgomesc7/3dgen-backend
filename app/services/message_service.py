from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate


class MessageService:
    def __init__(self, session: Session):
        self._db = session

    def create(self, data: MessageCreate) -> Message:
        message = Message(
            chat_id=data.chat_id,
            role=data.role,
            content=data.content,
        )
        self._db.add(message)
        self._db.commit()
        self._db.refresh(message)
        return message
