from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_DESCRIPTION_LEN = 3000
MIN_DESCRIPTION_LEN = 1


class WrongDescriptionValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class DCDescription(ValueObject[str | None]):
    def _validate(self) -> None:
        pass
