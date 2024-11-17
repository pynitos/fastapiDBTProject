from dataclasses import dataclass

from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.value_objects.emotion.description import EmotionDescription
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName


@dataclass
class EmotionDM:
    id: EmotionId
    name: EmotionName
    description: EmotionDescription = None

    @classmethod
    def create(cls, command: CreateEmotionCommand):
        emotion = cls(
            id=command.id,
            name=EmotionName(command.name),
            description=EmotionDescription(command.description)
        )
        return emotion
