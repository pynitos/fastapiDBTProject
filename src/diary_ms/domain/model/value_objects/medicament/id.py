from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from src.diary_ms.domain.common.model.value_objects.base import ValueObject
from src.diary_ms.domain.common.types.id import TypeId


@dataclass(frozen=True)
class MedicamentId(ValueObject[UUID | None]):
    def _validate(self) -> None:
        pass
