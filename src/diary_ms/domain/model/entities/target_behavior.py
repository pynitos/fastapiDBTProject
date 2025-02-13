from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.action import TargetAction
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge


@dataclass
class Target(BaseEntity):
    id: TargetId
    user_id: UserId
    urge: TargetUrge
    action: TargetAction
    is_default: TargetIsDefault = TargetIsDefault(False)

    @classmethod
    def create(
        cls,
        id: TargetId,
        user_id: UserId,
        urge: TargetUrge,
        action: TargetAction,
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

    @classmethod
    def admin_create(
        cls,
        id: TargetId,
        user_id: UserId,
        urge: TargetUrge,
        action: TargetAction,
        is_default: TargetIsDefault,
    ) -> Self:
        if not user_id.value:
            raise UserIdNotProvidedError
        t = cls(
            id=id,
            user_id=user_id,
            urge=urge,
            action=action,
            is_default=is_default,
        )
        return t

    def update(
        self,
        urge: TargetUrge | None = None,
        action: TargetAction | None = None,
    ) -> Self:
        if urge:
            self.urge = urge
        if action:
            self.action = action
        return self
