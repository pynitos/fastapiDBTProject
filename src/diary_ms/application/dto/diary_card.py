from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.diary_ms.application.dto.pagination import Pagination


@dataclass
class TargetDTO:
    urge: str
    action: str


@dataclass
class EmotionDTO:
    name: str
    description: str


@dataclass
class MedicamentDTO:
    name: str
    dosage: str


@dataclass
class SkillDTO:
    category: str
    group: str
    name: str


@dataclass
class OwnDiaryCardDTO:
    id: UUID
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[TargetDTO] | None = None
    emotions: list[EmotionDTO] | None = None
    medicaments: list[MedicamentDTO] | None = None
    skills: list[SkillDTO] | None = None


@dataclass
class GetOwnDiaryCardsDTO:
    pagination: Pagination


@dataclass
class GetOwnDiaryCardDTO:
    id: UUID
