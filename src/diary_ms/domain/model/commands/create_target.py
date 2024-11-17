from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class CreateTargetCommand:
    user_id: UserId
    urge: str
    action: str
    id: TargetId | None = None
