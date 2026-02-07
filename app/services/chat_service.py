import math
from typing import Optional
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.schemas.chat import ChatCreate
from app.exceptions.base import NotFoundException


class ChatService:
    def __init__(self, session: Session):
        self._db = session

    def create(self, data: ChatCreate) -> Chat:
        title = ""
        if data.user_prompt:
            title = self._generate_chat_title(data.user_prompt, 50)

        chat = Chat(user_id=data.user_id, name=title)
        self._db.add(chat)
        self._db.commit()
        self._db.refresh(chat)
        return chat

    def get(self, chat_id: int) -> Chat | None:
        return self._db.query(Chat).filter(Chat.id == chat_id).first()

    def list(self) -> list[Chat]:
        return self._db.query(Chat).order_by(Chat.created_at.desc()).all()

    def update_name(self, chat_id: int, new_name: str) -> Chat:
        chat = self.get(chat_id)

        if not chat:
            raise NotFoundException(f"Chat with ID {chat_id} not found.")

        chat.name = new_name
        self._db.commit()
        self._db.refresh(chat)
        return chat

    def delete(self, chat_id: int) -> None:
        chat = self.get(chat_id)

        if not chat:
            raise NotFoundException(f"Chat with ID {chat_id} not found.")

        self._db.delete(chat)
        self._db.commit()

    def paginated_list(
        self,
        page: int,
        page_size: int,
        user_id: Optional[int] = None,
    ):
        offset = (page - 1) * page_size

        query = self._db.query(Chat)

        if user_id is not None:
            query = query.filter(Chat.user_id == user_id)

        total = query.count()

        items = (
            query
            .order_by(Chat.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": math.ceil(total / page_size),
        }


    @staticmethod
    def _generate_chat_title(text: str, max_length: int = 50) -> str:
        text = text.strip()

        if len(text) <= max_length:
            return text

        cut = text[:max_length]
        return cut.rsplit(" ", 1)[0]
