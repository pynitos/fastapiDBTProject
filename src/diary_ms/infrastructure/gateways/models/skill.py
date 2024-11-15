from typing import TYPE_CHECKING

from sqlmodel import Relationship

from src.diary_ms.infrastructure.gateways.models.base import Base
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCardSkillLink

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class Skill(Base, table=True):
    category: str
    group: str
    name: str
    type: str = 'dbt'

    diary_cards: list["DiaryCard"] | None = Relationship(back_populates="skills", link_model=DiaryCardSkillLink)
