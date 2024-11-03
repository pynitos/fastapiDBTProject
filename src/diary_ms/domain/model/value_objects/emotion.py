from dataclasses import dataclass

from src.diary_ms.domain.common.types.id import TypeId


@dataclass
class EmotionDM:
    id: TypeId
    name: str
    description: str = None
