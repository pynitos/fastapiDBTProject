from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_URGE_LEN = 200
MIN_URGE_LEN = 3


class WrongTargetUrgeValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class TargetUrge(ValueObject[str]):
    def _validate(self) -> None:
        pass
