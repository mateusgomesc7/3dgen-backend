from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.provider import Provider
    from app.models.message import Message


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("providers.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    last_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    provider: Mapped["Provider"] = relationship(
        "Provider",
        back_populates="models"
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="model"
    )
