from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.entities.coping_strategy import CopingStrategy
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge


@dataclass
class Target(BaseEntity):
    user_id: UserId
    urge: TargetUrge
    action: CopingAction = CopingAction()
    coping_strategy: CopingStrategy | None = None
    is_default: TargetIsDefault = TargetIsDefault(False)
    id: TargetId = TargetId(None)

    @classmethod
    def create(
        cls,
        id: TargetId,
        user_id: UserId,
        urge: TargetUrge,
        action: CopingAction,
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
        action: CopingAction,
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
        action: CopingAction | None = None,
    ) -> Self:
        if urge:
            self.urge = urge
        if action:
            self.action = action
        return self
