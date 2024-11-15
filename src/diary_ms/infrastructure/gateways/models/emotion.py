from typing import TYPE_CHECKING

from sqlmodel import Relationship

from src.diary_ms.infrastructure.gateways.models.base import Base
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard, DiaryCardEmotionLink
if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class Emotion(Base, table=True):
    name: str
    description: str = None

    diary_cards: list["DiaryCard"] | None = Relationship(back_populates="emotions", link_model=DiaryCardEmotionLink)

