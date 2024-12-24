from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.diary_ms.infrastructure.gateways.models.base import BaseMixin

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class Medicament(BaseMixin):
    __tablename__ = "medicaments"

    user_id: Mapped[UUID]
    name: Mapped[str] = mapped_column(String(20))
    dosage: Mapped[str] = mapped_column(String(20))

    diary_cards: Mapped[list["DiaryCard"] | None] = relationship(
        back_populates="medicaments", secondary="DiaryCardMedicament"
    )
