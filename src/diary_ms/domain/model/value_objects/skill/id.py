from dataclasses import dataclass

from src.diary_ms.domain.common.model.value_objects.base import ValueObject
from src.diary_ms.domain.common.types.id import TypeId


@dataclass(frozen=True)
class SkillId(ValueObject[TypeId | None]):
    def __composite_values__(self) -> tuple[str]:
        return (str(self.value),)
