from dataclasses import dataclass

from diary_ms.domain.common.exceptions.base import DomainValueError
from diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_MOOD_VALUE = 5
MIN_MOOD_VALUE = 0


class WrongMoodValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class DCMood(ValueObject[int]):
    def _validate(self) -> None:
        if self.value > MAX_MOOD_VALUE:
            raise WrongMoodValueError(
                f"Mood must be lower or equal {MAX_MOOD_VALUE}, you have {self.value}",
            )
        if self.value < MIN_MOOD_VALUE:
            raise WrongMoodValueError(
                f"Mood must be greater or equal {
                    MIN_MOOD_VALUE
                    }, you have {self.value}",
            )
