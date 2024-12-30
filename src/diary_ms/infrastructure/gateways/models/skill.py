from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.infrastructure.gateways.models.base import BaseMixin

if TYPE_CHECKING:
    pass


class Skill(BaseMixin):
    __tablename__ = "skills"

    category: Mapped[str] = mapped_column(String(20))
    group: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(20))
    type: Mapped[str] = mapped_column(String(20), default=SkillType.DBT)
