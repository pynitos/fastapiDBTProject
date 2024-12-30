from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.diary_ms.infrastructure.gateways.models.base import BaseMixin

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.diary_card import (
        DiaryCardTarget,  # noqa: F401
    )


class Target(BaseMixin):
    __tablename__ = "targets"

    user_id: Mapped[UUID]
    urge: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(200))
