from dataclasses import dataclass
from uuid import UUID

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class SkillAdminDTO:
    id: UUID
    name: str
    category: str | None = None
    group: str | None = None
    type: SkillType = SkillType.DBT
    description: str | None = None


@dataclass
class GetSkillAdminDTO:
    id: UUID


@dataclass
class SkillsAdminFilters:
    type: SkillType | None = SkillType.DBT


@dataclass
class GetSkillsAdminDTO:
    pagination: Pagination
    filters: SkillsAdminFilters
