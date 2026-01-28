import math
from typing import Optional
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate


class ChatService:
    def __init__(self, session: Session):
        self._db = session

    def create(self, data: ChatCreate) -> Chat:
        chat = Chat(
            user_id=data.user_id,
            assistant_id=data.assistant_id,
        )
        self._db.add(chat)
        self._db.commit()
        self._db.refresh(chat)
        return chat

    def get(self, chat_id: int) -> Chat | None:
        return self._db.query(Chat).filter(Chat.id == chat_id).first()

    def list(self) -> list[Chat]:
        return self._db.query(Chat).order_by(Chat.created_at.desc()).all()

    def update(self, chat: Chat, data: ChatUpdate) -> Chat:
        if data.assistant_id is not None:
            chat.assistant_id = data.assistant_id

        self._db.commit()
        self._db.refresh(chat)
        return chat

    def delete(self, chat: Chat) -> None:
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
