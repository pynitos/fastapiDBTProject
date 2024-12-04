from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.value_objects.base import ValueObject


@dataclass(frozen=True)
class MedicamentId(ValueObject[UUID | None]):
    def _validate(self) -> None:
        pass
