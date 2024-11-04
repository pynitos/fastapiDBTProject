from dataclasses import dataclass
from typing import NewType

from src.diary_ms.domain.common.types.id import TypeId

SkillId = NewType('SkillId', TypeId)


@dataclass
class SkillDM:
    id: SkillId
    category: str
    group: str
    name: str
    type: str = 'dbt'
