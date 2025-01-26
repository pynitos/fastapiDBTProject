from dataclasses import dataclass

from src.diary_ms.domain.common.exceptions.base import DomainValueError
from src.diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_CATEGORY_VALUE = 200
MIN_CATEGORY_VALUE = 3


class WrongSkillCategoryValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillCategory(ValueObject[str | None]):
    def _validate(self) -> None:
        pass
