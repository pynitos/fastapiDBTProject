from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_DESCRIPTION_VALUE = 200
MIN_DESCRIPTION_VALUE = 2


class WrongSkillSituationValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillUsage(ValueObject[str]):
    def _validate(self) -> None:
        pass
