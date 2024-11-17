from src.diary_ms.domain.model.entities.target_behavior import TargetId
from src.diary_ms.domain.model.entities.user_id import UserId


class CreateTargetCommand:
    user_id: UserId
    urge: str
    action: str

    id: TargetId | None = None
