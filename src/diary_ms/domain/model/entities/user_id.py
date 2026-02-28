from dataclasses import dataclass

from diary_ms.domain.common.model.value_objects.base import ValueObject
from diary_ms.domain.common.types.id import TypeId


@dataclass(frozen=True)
class UserId(ValueObject[TypeId]):
    def __composite_values__(self) -> tuple[str]:
        return (str(self.value),)
