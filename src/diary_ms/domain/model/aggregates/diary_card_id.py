from dataclasses import dataclass

from src.diary_ms.domain.common.model.value_objects.base import ValueObject
from src.diary_ms.domain.common.types.id import TypeId


@dataclass(frozen=True)
class DiaryCardId(ValueObject[TypeId | None]):
    pass
