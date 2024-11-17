from dataclasses import dataclass
from typing import Self

from src.diary_ms.domain.model.commands.create_skill import CreateSkillCommand
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class SkillDM:
    id: SkillId | None
    category: SkillCategory
    group: SkillGroup
    name: SkillName
    type: SkillType = SkillType.DBT

    @classmethod
    def create(cls, command: CreateSkillCommand) -> Self:
        skill = cls(
            id=command.id,
            category=SkillCategory(command.category),
            group=SkillGroup(command.group),
            name=SkillName(command.name),
            type=command.type,
        )
        return skill
