from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.diary_ms.infrastructure.gateways.models.base import BaseMixin
from src.diary_ms.infrastructure.gateways.models.diary_card import (
    DiaryCard,
)

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class Emotion(BaseMixin):
    __tablename__ = "emotions"

    name: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(String(100), default=None)

    diary_cards: Mapped[list["DiaryCard"] | None] = relationship(
        back_populates="emotions", secondary="DiaryCardEmotion"
    )
