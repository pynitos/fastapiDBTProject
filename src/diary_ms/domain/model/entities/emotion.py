from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.exceptions.access import AuthenticationError
from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName


@dataclass
class EmotionDM(BaseEntity):
    name: EmotionName
    user_id: UserId
    id: EmotionId = EmotionId(value=None)
    description: EmotionDescription = EmotionDescription(value=None)

    @classmethod
    def create(cls, command: CreateEmotionCommand) -> Self:
        if not command.user_id:
            raise UserIdNotProvidedError
        emotion = cls(
            id=EmotionId(None),
            user_id=UserId(command.user_id),
            name=EmotionName(command.name),
            description=EmotionDescription(command.description),
        )
        return emotion
