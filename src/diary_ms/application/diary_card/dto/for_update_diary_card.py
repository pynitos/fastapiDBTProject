from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class TargetForUpdDTO(DTO):
    id: UUID
    urge: str
    action: str


@dataclass
class EmotionForUpdDTO(DTO):
    id: UUID
    name: str
    description: str | None


@dataclass
class MedicamentForUpdDTO(DTO):
    id: UUID
    name: str
    dosage: str


@dataclass
class SkillForUpdDTO(DTO):
    id: UUID
    category: str | None
    group: str | None
    name: str


@dataclass
class DiaryCardForUpdateDTO(DTO):
    id: UUID
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: date | None = None
    type_: SkillType = SkillType.DBT
    targets: list[TargetForUpdDTO] | None = None
    emotions: list[EmotionForUpdDTO] | None = None
    medicaments: list[MedicamentForUpdDTO] | None = None
    skills: list[SkillForUpdDTO] | None = None
    # For choice:
    all_targets: list[TargetForUpdDTO] | None = None
    all_emotions: list[EmotionForUpdDTO] | None = None
    all_medicaments: list[MedicamentForUpdDTO] | None = None
    all_skills: list[SkillForUpdDTO] | None = None


@dataclass
class GetDiaryCardForUpdateDTO(Query):
    id: UUID
