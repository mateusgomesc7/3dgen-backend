from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from .base import TimestampMixin


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    role: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column(Text)

    chat = relationship("Chat", back_populates="messages")
