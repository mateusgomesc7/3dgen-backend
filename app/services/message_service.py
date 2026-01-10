from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.message import Message
from app.models.chat import Chat
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

    def list_by_chat(self, chat_id: int) -> list[Message]:
        chat_exists = (
            self._db.query(Chat.id)
            .filter(Chat.id == chat_id)
            .first()
        )

        if not chat_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        return (
            self._db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )
