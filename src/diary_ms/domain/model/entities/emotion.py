import uuid
from dataclasses import dataclass, field
from typing import Self

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName


@dataclass
class Emotion(BaseEntity):
    name: EmotionName
    id: EmotionId = field(default_factory=lambda: EmotionId(uuid.uuid4()))
    description: EmotionDescription | None = None

    @classmethod
    def create(cls, name: EmotionName, description: EmotionDescription) -> Self:
        emotion = cls(
            name=name,
            description=description,
        )
        return emotion

    def update(
        self,
        name: EmotionName | None = None,
        description: EmotionDescription | None = None,
    ) -> Self:
        if name:
            self.name = name
        if description:
            self.description = description
        return self
