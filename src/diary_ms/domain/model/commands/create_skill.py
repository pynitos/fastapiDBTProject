from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


class CreateSkillCommand:
    category: str
    group: str
    name: str
    type: SkillType = SkillType.DBT

    id: SkillId | None = None
