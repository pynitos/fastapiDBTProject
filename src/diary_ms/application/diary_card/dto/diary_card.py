from dataclasses import dataclass
from datetime import date
from uuid import UUID

from diary_ms.application.common.dto.base import ResultDTO
from diary_ms.application.common.dto.pagination import Pagination
from diary_ms.application.common.dto.query import Query
from diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class TargetResultDTO(ResultDTO):
    id: UUID
    user_id: UUID
    urge: str
    urge_intensity: int | None = None
    action: str | None = None
    effectiveness: int | None = None


@dataclass
class EmotionResultDTO(ResultDTO):
    id: UUID
    name: str
    description: str | None


@dataclass
class MedicamentResultDTO(ResultDTO):
    id: UUID
    user_id: UUID
    name: str
    dosage: str | None


@dataclass
class SkillResultDTO(ResultDTO):
    id: UUID
    category: str | None
    group: str | None
    name: str
    usage: str | None
    effectiveness: int | None


@dataclass
class OwnDiaryCardResultDTO(ResultDTO):
    id: UUID
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[TargetResultDTO] | None = None
    emotions: list[EmotionResultDTO] | None = None
    medicaments: list[MedicamentResultDTO] | None = None
    skills: list[SkillResultDTO] | None = None
    type: SkillType = SkillType.DBT


@dataclass
class OwnDiaryCardsResultDTO(ResultDTO):
    diary_cards: list[OwnDiaryCardResultDTO]
    total: int


@dataclass
class GetOwnDiaryCardsQuery(Query[OwnDiaryCardsResultDTO]):
    pagination: Pagination


@dataclass
class GetOwnDiaryCardQuery(Query[OwnDiaryCardResultDTO]):
    id: UUID
