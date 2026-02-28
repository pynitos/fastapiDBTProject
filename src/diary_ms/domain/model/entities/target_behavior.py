import uuid
from dataclasses import dataclass, field
from typing import Self

from diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from diary_ms.domain.common.model.entities.base import BaseEntity
from diary_ms.domain.model.entities.coping_strategy import CopingStrategy
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge


@dataclass
class Target(BaseEntity):
    user_id: UserId
    urge: TargetUrge
    id: TargetId = field(default_factory=lambda: TargetId(uuid.uuid4()))
    action: CopingAction | None = None
    coping_strategy: CopingStrategy | None = None
    is_default: TargetIsDefault = TargetIsDefault(False)

    @classmethod
    def create(
        cls,
        id: TargetId,
        user_id: UserId,
        urge: TargetUrge,
        action: CopingAction | None = None,
    ) -> Self:
        if not user_id.value:
            raise UserIdNotProvidedError
        t = cls(
            id=id,
            user_id=user_id,
            urge=urge,
            action=action,
        )
        return t

    def update(
        self,
        urge: TargetUrge | None = None,
        action: CopingAction | None = None,
    ) -> Self:
        if urge:
            self.urge = urge
        if action:
            self.action = action
        return self
