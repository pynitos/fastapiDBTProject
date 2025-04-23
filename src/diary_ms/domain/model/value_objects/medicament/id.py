from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.domain.common.model.value_objects.base import ValueObject


@dataclass(frozen=True)
class MedicamentId(ValueObject[UUID]):
    def __composite_values__(self) -> tuple[str | None]:
        return (str(self.value) if self.value else None,)
