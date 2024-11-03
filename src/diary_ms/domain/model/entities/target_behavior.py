from dataclasses import dataclass

from src.diary_ms.domain.common.model.base import BaseDM
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.weekday import Weekday


@dataclass
class TargetBehaviorDM(BaseDM):
    user_id: UserId
    urge: str
    action: str
