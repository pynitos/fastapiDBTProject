from dataclasses import dataclass

from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


@dataclass
class CreateTargetCommand:
    urge: str
    action: str
    id: TargetId | None = None
    user_id: UserId | None = None
