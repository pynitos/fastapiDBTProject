from dataclasses import dataclass

from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


@dataclass
class CreateEmotionCommand:
    name: str
    description: str | None = None
