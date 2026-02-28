from dataclasses import dataclass, field
from datetime import date

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_DATE_VALUE = 5
MIN_DATE_VALUE = 0


class WrongDateOfEntryValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class DCDateOfEntry(ValueObject[date]):
    value: date = field(default_factory=date.today)

    def _validate(self) -> None:
        pass
