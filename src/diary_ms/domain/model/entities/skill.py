import uuid
from dataclasses import dataclass, field
from typing import Self

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class Skill(BaseEntity):
    name: SkillName
    id: SkillId = field(default_factory=lambda: SkillId(uuid.uuid4()))
    category: SkillCategory | None = None
    group: SkillGroup | None = None
    type: SkillType = SkillType.DBT
    description: SkillDescription | None = None

    @classmethod
    def create(
        cls,
        id: SkillId,
        name: SkillName,
        category: SkillCategory | None = None,
        group: SkillGroup | None = None,
        description: SkillDescription | None = None,
        skill_type: SkillType = SkillType.DBT,
    ) -> Self:
        skill = cls(
            id=id,
            category=category,
            group=group,
            name=name,
            type=skill_type,
            description=description,
        )
        return skill

    def update(
        self,
        name: SkillName | None = None,
        category: SkillCategory | None = None,
        group: SkillGroup | None = None,
        description: SkillDescription | None = None,
        skill_type: SkillType | None = None,
    ) -> Self:
        if category:
            self.category = category
        if group:
            self.group = group
        if name:
            self.name = name
        if skill_type:
            self.type = skill_type
        if description:
            self.description = description
        return self
