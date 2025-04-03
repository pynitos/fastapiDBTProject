from enum import Enum


class MoodDisplay(Enum):
    VERY_BAD = ("😞", "Очень плохое")
    BAD = ("😕", "Плохое")
    NEUTRAL = ("😐", "Нейтральное")
    GOOD = ("😊", "Хорошее")
    EXCELLENT = ("😄", "Отличное")

    @property
    def emoji(self) -> str:
        return self.value[0]

    @property
    def text(self) -> str:
        return self.value[1]

    @classmethod
    def from_level(cls, level: int) -> "MoodDisplay":
        return {1: cls.VERY_BAD, 2: cls.BAD, 3: cls.NEUTRAL, 4: cls.GOOD, 5: cls.EXCELLENT}[level]
