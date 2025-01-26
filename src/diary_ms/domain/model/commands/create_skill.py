from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class CreateSkillCommand:
    category: str
    group: str
    name: str
    type: SkillType = SkillType.DBT

    id: UUID | None = None
    description: SkillDescription | None = None
