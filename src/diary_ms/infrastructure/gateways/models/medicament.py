from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Relationship

from src.diary_ms.infrastructure.gateways.models.base import Base
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCardMedicamentLink
if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class Medicament(Base, table=True):
    user_id: UUID
    name: str
    dosage: str

    diary_cards: list["DiaryCard"] | None = Relationship(back_populates="medicaments", link_model=DiaryCardMedicamentLink)


