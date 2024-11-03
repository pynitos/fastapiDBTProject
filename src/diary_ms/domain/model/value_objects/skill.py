from dataclasses import dataclass

from src.diary_ms.domain.common.types.id import TypeId


@dataclass
class SkillDM:
    id: TypeId
    category: str
    group: str
    name: str
    type: str = 'dbt'
