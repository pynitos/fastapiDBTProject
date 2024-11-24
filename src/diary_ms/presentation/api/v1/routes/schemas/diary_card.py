from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicament import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM


class DiaryCardReq(BaseModel):
    mood: int
    description: str | None = None
    date_of_entry: date = Field(default_factory=date.today)

    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[MedicamentDM] | None = None
    skills: list[SkillDM] | None = None


class CreateDiaryCardReq(BaseModel):
    mood: int
    description: str | None = None
    date_of_entry: date = Field(default_factory=date.today)

    targets: list[UUID] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[UUID] | None = None


class UpdateDiaryCardReq(BaseModel):
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None

    targets: list[UUID] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[UUID] | None = None
