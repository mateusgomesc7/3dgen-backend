from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.message import Message
from app.models.chat import Chat
from app.schemas.message import MessageCreate


class MessageService:
    def __init__(self, session: Session):
        self._db = session

    def create_with_response(self, data: MessageCreate) -> list[Message]:
        if data.chat_id is None:
            chat = Chat()
            self._db.add(chat)
            self._db.commit()
            self._db.refresh(chat)
            chat_id = chat.id
        else:
            chat = self._db.query(Chat).filter(Chat.id == data.chat_id).first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat not found",
                )
            chat_id = chat.id

        user_message = Message(
            chat_id=chat_id,
            role="user",
            content=data.content,
        )
        self._db.add(user_message)
        self._db.commit()
        self._db.refresh(user_message)

        assistant_message = Message(
            chat_id=chat_id,
            role="assistant",
            content=self._fake_ai_response(data.content),
        )
        self._db.add(assistant_message)
        self._db.commit()
        self._db.refresh(assistant_message)

        return [user_message, assistant_message]

    def _fake_ai_response(self, prompt: str) -> str:
        return f"🤖 Fake response to: '{prompt}'"

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
