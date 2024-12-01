from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName


@dataclass
class EmotionDM:
    name: EmotionName
    id: EmotionId = EmotionId(value=None)
    description: EmotionDescription = EmotionDescription(value=None)

    @classmethod
    def create(cls, command: CreateEmotionCommand) -> Self:
        emotion = cls(
            id=EmotionId(None),
            name=EmotionName(command.name),
            description=EmotionDescription(command.description),
        )
        return emotion
