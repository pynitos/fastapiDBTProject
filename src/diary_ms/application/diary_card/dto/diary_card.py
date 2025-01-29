from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class TargetDTO(DTO):
    urge: str
    action: str


@dataclass
class EmotionDTO(DTO):
    name: str
    description: str | None


@dataclass
class MedicamentDTO(DTO):
    name: str
    dosage: str


@dataclass
class SkillDTO(DTO):
    category: str
    group: str
    name: str
    situation: str | None


@dataclass
class OwnDiaryCardDTO(DTO):
    id: UUID
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[TargetDTO] | None = None
    emotions: list[EmotionDTO] | None = None
    medicaments: list[MedicamentDTO] | None = None
    skills: list[SkillDTO] | None = None
    type: SkillType = SkillType.DBT


@dataclass
class GetOwnDiaryCardsDTO(DTO):
    pagination: Pagination


@dataclass
class GetOwnDiaryCardDTO(DTO):
    id: UUID
