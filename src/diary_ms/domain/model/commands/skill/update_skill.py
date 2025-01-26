from dataclasses import dataclass

from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class UpdateSkillAdminCommand:
    name: str | None = None
    category: str | None = None
    group: str | None = None
    type: SkillType | None = None
    description: str | None = None
