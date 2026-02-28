from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_SKILL_EFFECTIVENESS_VALUE = 7
MIN_SKILL_EFFECTIVENESS_VALUE = 0


class WrongSkillEffectivenessValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class SkillEffectiveness(ValueObject[int]):
    def _validate(self) -> None:
        if not MIN_SKILL_EFFECTIVENESS_VALUE <= self.value <= MAX_SKILL_EFFECTIVENESS_VALUE:
            raise WrongSkillEffectivenessValueError(
                f"Effectiveness must be {MIN_SKILL_EFFECTIVENESS_VALUE}-{MAX_SKILL_EFFECTIVENESS_VALUE}"
            )

    def is_effective(self) -> bool:
        return self.value > 3
