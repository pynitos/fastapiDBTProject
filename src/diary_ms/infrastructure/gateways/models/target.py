from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Relationship

from src.diary_ms.infrastructure.gateways.models.base import Base
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCardTargetLink

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class Target(Base, table=True):
    user_id: UUID
    urge: str
    action: str

    diary_cards: list["DiaryCard"] | None = Relationship(back_populates="targets", link_model=DiaryCardTargetLink)
