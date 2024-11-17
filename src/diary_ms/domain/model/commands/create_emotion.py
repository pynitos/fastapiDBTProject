from src.diary_ms.domain.model.entities.emotion import EmotionId


class CreateEmotionCommand:
    name: str
    description: str = None

    id: EmotionId | None = None
