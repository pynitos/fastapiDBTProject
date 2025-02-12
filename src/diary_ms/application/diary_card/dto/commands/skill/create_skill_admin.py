from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class CreateSkillAdminCommand(Command[None]):
    name: str
    id: UUID | None = None
    category: str | None = None
    group: str | None = None
    type: SkillType = SkillType.DBT
    description: str | None = None
