from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


class CreateEmotionCommand:
    name: str
    description: str = None

    id: EmotionId | None = None
