from dataclasses import dataclass
from datetime import date

from src.diary_ms.domain.common.exceptions.base import DomainValueError
from src.diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_DATE_VALUE = 5
MIN_DATE_VALUE = 0


class WrongDateOfEntryValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class DCDateOfEntry(ValueObject[date]):
    def _validate(self) -> None:
        pass
