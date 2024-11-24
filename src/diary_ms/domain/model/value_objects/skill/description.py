from dataclasses import dataclass

from src.diary_ms.domain.common.exceptions.base import DomainValueError
from src.diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_DESCRIPTION_VALUE = 200
MIN_DESCRIPTION_VALUE = 3


class WrongSkillDescriptionValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillDescription(ValueObject[str]):
    def _validate(self) -> None:
        pass
