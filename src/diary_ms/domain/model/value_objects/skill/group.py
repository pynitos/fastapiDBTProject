from dataclasses import dataclass

from src.diary_ms.domain.common.exceptions.base import DomainValueError
from src.diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_SKILL_GROUP_VALUE = 200
MIN_SKILL_GROUP_VALUE = 3


class WrongSkillGroupValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillGroup(ValueObject[str]):
    def _validate(self) -> None:
        pass
