from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.target_behavior.create_target import (
    CreateTargetAdminCommand,
    CreateTargetCommand,
)
from src.diary_ms.domain.model.commands.target_behavior.update_target import (
    UpdateTargetAdminCommand,
    UpdateTargetCommand,
)
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
    def create(cls, command: CreateTargetCommand | CreateTargetAdminCommand) -> Self:
        if not command.user_id:
            raise UserIdNotProvidedError
        t = cls(
            id=TargetId(command.id),
            user_id=UserId(command.user_id),
            urge=TargetUrge(command.urge),
            action=TargetAction(command.action),
        )
        return t

    def update(self, command: UpdateTargetCommand | UpdateTargetAdminCommand) -> Self:
        if command.urge:
            self.urge = TargetUrge(command.urge)
        if command.action:
            self.action = TargetAction(command.action)
        return self
