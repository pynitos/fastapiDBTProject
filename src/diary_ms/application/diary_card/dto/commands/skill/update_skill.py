from dataclasses import dataclass
from uuid import UUID

from diary_ms.application.common.dto.command import Command
from diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class UpdateSkillAdminCommand(Command[None]):
    id: UUID
    name: str | None = None
    category: str | None = None
    group: str | None = None
    type: SkillType | None = None
    description: str | None = None
