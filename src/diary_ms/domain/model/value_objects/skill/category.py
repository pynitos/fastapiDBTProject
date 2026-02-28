from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_CATEGORY_VALUE = 200
MIN_CATEGORY_VALUE = 3


class WrongSkillCategoryValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillCategory(ValueObject[str]):
    def _validate(self) -> None:
        pass
