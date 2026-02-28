from dataclasses import dataclass
from enum import Enum
from typing import Self

from diary_ms.domain.common.model.value_objects.base import ValueObject

MIN_URGE_INTENSITY = 0  # 0 = "нет побуждения"
MAX_URGE_INTENSITY = 5


class UrgeIntensityLevel(Enum):
    NONE = (0, {"en": "No urge", "ru": "Нет побуждения"})
    VERY_MILD = (1, {"en": "Very mild", "ru": "Очень слабое"})
    MILD = (2, {"en": "Mild", "ru": "Слабое"})
    MODERATE = (3, {"en": "Moderate", "ru": "Умеренное"})
    STRONG = (4, {"en": "Strong", "ru": "Сильное"})
    VERY_STRONG = (5, {"en": "Very strong", "ru": "Очень сильное"})

    @classmethod
    def from_intensity(cls, value: int) -> "UrgeIntensityLevel":
        """Возвращает уровень интенсивности по числовому значению.

        Args:
            value: Числовое значение интенсивности (0-5)

        Returns:
            Соответствующий уровень интенсивности или NONE, если значение не найдено.
        """
        try:
            return cls(value)  # Используем встроенный механизм Enum
        except ValueError:
            return cls.NONE  # Возвращаем NONE для любых невалидных значений

    def describe(self, lang: str = "ru") -> str:
        """Возвращает локализованное описание уровня интенсивности.
        Args:
            lang: Код языка ('ru' или 'en')
        Returns:
            Описание на указанном языке или русском по умолчанию.
        """
        return self.value[1][lang]

    @property
    def is_strong(self) -> bool:
        return self.value[0] >= 4


@dataclass(frozen=True)
class UrgeIntensity(ValueObject[int]):
    def _validate(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("Intensity must be an integer")
        if not MIN_URGE_INTENSITY <= self.value <= MAX_URGE_INTENSITY:
            raise ValueError(f"Intensity must be {MIN_URGE_INTENSITY}-{MAX_URGE_INTENSITY}")

    @classmethod
    def create(cls, value: int | None) -> Self | None:
        """Фабричный метод с обработкой None и валидацией."""
        if value is None:
            return None
        return cls(value)  # Вызовет _validate автоматически

    def is_absent(self) -> bool:
        return self.value == 0

    def is_strong(self) -> bool:
        return self.value >= 4

    def describe(self, lang: str = "ru") -> str:
        return UrgeIntensityLevel.from_intensity(self.value).describe(lang)
