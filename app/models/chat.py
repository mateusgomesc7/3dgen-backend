from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from .base import TimestampMixin


class Chat(Base, TimestampMixin):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=True)

    user = relationship('User')
    messages = relationship(
        'Message', back_populates='chat', cascade='all, delete-orphan'
    )
