from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.emotion.create_emotion import CreateEmotionAdminCommand
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName


@dataclass
class Emotion(BaseEntity):
    name: EmotionName
    id: EmotionId | None = None
    description: EmotionDescription = EmotionDescription(value=None)

    @classmethod
    def create(cls, command: CreateEmotionAdminCommand) -> Self:
        emotion = cls(
            name=EmotionName(command.name),
            description=EmotionDescription(command.description),
        )
        return emotion
