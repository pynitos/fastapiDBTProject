from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class TargetDTO(ResultDTO):
    id: UUID
    user_id: UUID
    urge: str
    action: str | None = None
    effectiveness: int | None = None


@dataclass
class EmotionDTO(ResultDTO):
    id: UUID
    name: str
    description: str | None


@dataclass
class MedicamentDTO(ResultDTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str | None


@dataclass
class SkillDTO(ResultDTO):
    id: UUID
    category: str | None
    group: str | None
    name: str
    usage: str | None
    effectiveness: int | None


@dataclass
class OwnDiaryCardDTO(ResultDTO):
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
class GetOwnDiaryCardsDTO(Query[list[OwnDiaryCardDTO]]):
    pagination: Pagination


@dataclass
class GetOwnDiaryCardDTO(Query[OwnDiaryCardDTO]):
    id: UUID
