from dataclasses import dataclass

from src.diary_ms.domain.common.model.value_objects.base import ValueObject


@dataclass(frozen=True)
class CopingEffectiveness(ValueObject[int | None]):
    def _validate(self) -> None:
        pass
