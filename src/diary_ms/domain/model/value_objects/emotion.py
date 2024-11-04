from dataclasses import dataclass
from typing import NewType

from src.diary_ms.domain.common.types.id import TypeId

EmotionId = NewType('EmotionId', TypeId)


@dataclass
class EmotionDM:
    id: EmotionId
    name: str
    description: str = None
