from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from .base import TimestampMixin

if TYPE_CHECKING:
    from .model import Model


class Provider(Base, TimestampMixin):
    __tablename__ = 'providers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    models: Mapped[list['Model']] = relationship(
        'Model', back_populates='provider', cascade='all, delete-orphan'
    )
