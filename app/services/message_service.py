import re
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.message import Message
from app.models.chat import Chat
from app.ollama.ollama_client import OllamaClient
from app.ollama.validators import validate_threejs_code
from app.schemas.message import MessageCreate


class MessageService:
    def __init__(self, session: Session):
        self._db = session
        self._ollama = OllamaClient()
    
    @staticmethod
    def clean_ai_code(raw: str) -> str:
        raw = re.sub(r"```[a-zA-Z]*\n?", "", raw)
        raw = raw.replace("```", "")
        return raw.strip()
    
    def get_message(self, message_id: int) -> Message | None:
        return self._db.query(Message).filter(Message.id == message_id).first()

    def create_with_response(self, data: MessageCreate) -> Message:
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


        try:
            ai_response = self._ollama.generate_threejs(data.content)
            ai_response = self.clean_ai_code(ai_response)
            validate_threejs_code(ai_response)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ollama error: {str(e)}",
            )

        assistant_message = Message(
            chat_id=chat_id,
            role="assistant",
            content=ai_response,
        )
        self._db.add(assistant_message)
        self._db.commit()
        self._db.refresh(assistant_message)

        return assistant_message

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

    def update_message(self, message: Message, new_content: str) -> Message:
        message.content = new_content
        self._db.commit()
        self._db.refresh(message)
        return message