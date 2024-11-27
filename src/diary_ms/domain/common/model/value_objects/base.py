from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """This method checks that a value is valid to create this value object"""
        return None


@dataclass(frozen=True)
class ValueObject[V](BaseValueObject, ABC):
    value: V

    def to_raw(self) -> V:
        return self.value
