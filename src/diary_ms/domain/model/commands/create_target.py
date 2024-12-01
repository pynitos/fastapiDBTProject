from dataclasses import dataclass

from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


@dataclass
class CreateTargetCommand:
    urge: str
    action: str
    user_id: UserId
    id: TargetId | None = None
