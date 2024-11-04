from dataclasses import dataclass
from typing import NewType

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.common.types.id import TypeId

TargetId = NewType('TargetId', TypeId)


@dataclass
class TargetDM(BaseEntity):
    id: TargetId
    user_id: UserId
    urge: str
    action: str
