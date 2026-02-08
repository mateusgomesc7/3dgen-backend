from __future__ import annotations
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import TYPE_CHECKING

from app.models.model import Model
from app.models.message import Message
from app.models.chat import Chat
from app.schemas.message import MessageCreate
from app.services.assistants.factory import get_assistant
from app.services.ai.sanitizer import clean_ai_code
from app.services.ai.validator import validate_threejs_code

if TYPE_CHECKING:
    from app.services.assistants.base import AssistantClient


class MessageService:
    def __init__(self, session: Session):
        self._db = session


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

        model = self._db.query(Model).filter(Model.id == data.model_id).first()
        if not model or not model.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not found or inactive."
            )

        assistant_ai = get_assistant(provider=model.provider.name)
        history = self._get_formatted_history(chat_id, assistant_ai)

        user_message = Message(
            chat_id=chat_id,
            model_id=data.model_id,
            role="user",
            content=data.content,
        )
        self._db.add(user_message)
        self._db.commit()
        self._db.refresh(user_message)

        try:
            ai_response = assistant_ai.generate(
                content=data.content,
                history=history,
                model_name=model.name
            )
            ai_response = clean_ai_code(ai_response)
            validate_threejs_code(ai_response)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"{model.provider.name} error: {str(e)}",
            )

        assistant_message = Message(
            chat_id=chat_id,
            model_id=data.model_id,
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


    def _get_formatted_history(
            self,
            chat_id: int,
            assistant_ai: AssistantClient,
            limit: int = 6
    ) -> list[dict]:
        messages = (
            self._db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )

        formatted_history = []
        for msg in reversed(messages):
            formatted_history.append(assistant_ai.build_message_dict(msg.role, msg.content))
        return formatted_history
