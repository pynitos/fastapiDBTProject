from dataclasses import dataclass
from typing import Self
from uuid import uuid4

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.commands.create_skill import CreateSkillCommand
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class Skill(BaseEntity):
    id: SkillId = SkillId()
    category: SkillCategory = SkillCategory()
    group: SkillGroup = SkillGroup()
    name: SkillName = SkillName()
    type: SkillType = SkillType.DBT
    description: SkillDescription | None = None

    @classmethod
    def create(cls, command: CreateSkillCommand) -> Self:
        if not command.id:
            command.id = uuid4()
        skill = cls(
            id=SkillId(command.id),
            category=SkillCategory(command.category),
            group=SkillGroup(command.group),
            name=SkillName(command.name),
            type=SkillType(command.type),
            description=SkillDescription(command.description),
        )
        return skill
