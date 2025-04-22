from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Type

from src.diary_ms.domain.common.exceptions.base import DomainValueError
from src.diary_ms.domain.common.model.value_objects.base import ValueObject

MIN_INTENSITY = 1
MAX_INTENSITY = 5


class WrongTargetIntensityValueError(ValueError, DomainValueError):
    pass


class IntensityLevel(Enum):
    """Уровни интенсивности с многоязычными описаниями и значениями"""
    VERY_MILD = (1, {
        'en': "Very mild",
        'ru': "Очень слабое"
    })
    MILD = (2, {
        'en': "Mild",
        'ru': "Слабое"
    })
    MODERATE = (3, {
        'en': "Moderate",
        'ru': "Умеренное"
    })
    STRONG = (4, {
        'en': "Strong",
        'ru': "Сильное"
    })
    VERY_STRONG = (5, {
        'en': "Very strong",
        'ru': "Очень сильное"
    })

    def __init__(self, value: int, descriptions: Dict[str, str]):
        self._value_ = value
        self.descriptions = descriptions

    @classmethod
    def from_value(cls, value: int) -> Optional['IntensityLevel']:
        """Получение уровня интенсивности по числовому значению"""
        return next((level for level in cls if level.value == value), None)

    def describe(self, lang: str = 'ru') -> str:
        """Возвращает описание на указанном языке"""
        return self.descriptions.get(lang, self.descriptions['ru'])

    @classmethod
    def get_descriptions_map(cls) -> Dict[int, 'IntensityLevel']:
        """Возвращает словарь {значение: уровень}"""
        return {level.value: level for level in cls}


@dataclass(frozen=True)
class TargetIntensity(ValueObject[int]):
    """Value object для оценки интенсивности побуждения (1-5)"""
    
    def _validate(self) -> None:
        if not isinstance(self.value, int):
            raise WrongTargetIntensityValueError(
                f"Intensity must be integer, got {type(self.value)}"
            )
        
        if not MIN_INTENSITY <= self.value <= MAX_INTENSITY:
            raise WrongTargetIntensityValueError(
                f"Intensity must be between {MIN_INTENSITY} and {MAX_INTENSITY}, got {self.value}"
            )

    @classmethod
    def create(cls, value: Optional[int]) -> Optional['TargetIntensity']:
        """Фабричный метод с обработкой None"""
        if value is None:
            return None
        return cls(value)

    def is_strong_urge(self) -> bool:
        """Проверяет, является ли побуждение сильным (4-5)"""
        return self.value >= 4

    def describe(self, lang: str = 'ru') -> str:
        """Возвращает текстовое описание интенсивности"""
        level = IntensityLevel.from_value(self.value)
        return level.describe(lang) if level else "Неизвестная интенсивность"

    @property
    def level(self) -> Optional[IntensityLevel]:
        """Возвращает соответствующий Enum уровень"""
        return IntensityLevel.from_value(self.value)