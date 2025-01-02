from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.diary_ms.infrastructure.gateways.models.base import BaseMixin

if TYPE_CHECKING:
    pass


class Emotion(BaseMixin):
    __tablename__ = "emotions"

    user_id: Mapped[UUID]
    name: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(String(100), default=None)
