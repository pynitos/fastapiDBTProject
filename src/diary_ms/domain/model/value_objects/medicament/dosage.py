from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_DOSAGE_VALUE = 50
MIN_DOSAGE_VALUE = 2


class WrongMedicamentDosageValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class MedicamentDosage(ValueObject[str]):
    def _validate(self) -> None:
        """Валидация длины строки дозировки"""
        if not self.value:
            raise WrongMedicamentDosageValueError("Дозировка не может быть пустой")

        if len(self.value) < MIN_DOSAGE_VALUE:
            raise WrongMedicamentDosageValueError(
                f"Дозировка должна быть не короче {MIN_DOSAGE_VALUE} символов. " f"Получено: {len(self.value)}"
            )

        if len(self.value) > MAX_DOSAGE_VALUE:
            raise WrongMedicamentDosageValueError(
                f"Дозировка должна быть не длиннее {MAX_DOSAGE_VALUE} символов. " f"Получено: {len(self.value)}"
            )
