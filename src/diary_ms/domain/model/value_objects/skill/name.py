from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_SKILL_NAME_VALUE = 200
MIN_SKILL_NAME_VALUE = 3


class WrongSkillNameValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillName(ValueObject[str]):
    def _validate(self) -> None:
        pass
