from dataclasses import dataclass
from typing import NewType, Self

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.common.types.id import TypeId
from src.diary_ms.domain.model.commands.create_target import CreateTargetCommand
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.action import TargetAction
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge

TargetId = NewType('TargetId', TypeId)


@dataclass
class TargetDM(BaseEntity):
    id: TargetId
    user_id: UserId
    urge: TargetUrge
    action: TargetAction

    @classmethod
    def create(cls, command: CreateTargetCommand) -> Self:
        skill = cls(
            id=command.id,
            user_id=command.user_id,
            urge=TargetUrge(command.urge),
            action=TargetAction(command.action)
        )
        return skill
