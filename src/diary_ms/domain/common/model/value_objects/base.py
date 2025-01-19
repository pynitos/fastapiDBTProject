from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseValueObject(ABC):  # noqa: B024
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """This method checks that a value is valid to create this value object"""
        return None


@dataclass(frozen=True)
class ValueObject[V](BaseValueObject, ABC):
    value: V

    def to_raw(self) -> V:
        return self.value

    def __composite_values__(self) -> tuple[V]:
        return (self.value,)
