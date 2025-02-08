from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class TargetAdminDTO(DTO):
    id: UUID
    user_id: UUID
    urge: str
    action: str


@dataclass
class EmotionAdminDTO(DTO):
    id: UUID
    name: str
    description: str | None


@dataclass
class MedicamentAdminDTO(DTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str


@dataclass
class SkillAdminDTO(DTO):
    category: str | None
    group: str | None
    name: str
    situation: str | None


@dataclass
class DiaryCardAdminDTO(DTO):
    id: UUID
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[TargetAdminDTO] | None = None
    emotions: list[EmotionAdminDTO] | None = None
    medicaments: list[MedicamentAdminDTO] | None = None
    skills: list[SkillAdminDTO] | None = None
    type: SkillType = SkillType.DBT


@dataclass
class GetDiaryCardsAdminDTO(Query[list[DiaryCardAdminDTO]]):
    pagination: Pagination


@dataclass
class GetDiaryCardAdminDTO(Query[DiaryCardAdminDTO]):
    id: UUID
