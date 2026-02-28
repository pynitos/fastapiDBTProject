from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from diary_ms.domain.model.entities.emotion import Emotion
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.skill import Skill
from diary_ms.domain.model.entities.target_behavior import Target
from diary_ms.domain.model.value_objects.skill.type import SkillType


class DiaryCardReq(BaseModel):
    mood: int
    description: str | None = None
    date_of_entry: date = Field(default_factory=date.today)
    type: SkillType = SkillType.DBT

    targets: list[Target] | None = None
    emotions: list[Emotion] | None = None
    medicaments: list[Medicament] | None = None
    skills: list[Skill] | None = None


class DiaryCardSkillReq(BaseModel):
    skill_id: UUID
    usage: str | None = None
    effectiveness: int | None = None


class DiaryCardTargetReq(BaseModel):
    target_id: UUID
    urge_intensity: int | None = None
    action: str | None = None
    effectiveness: int | None = None


class CreateDiaryCardReq(BaseModel):
    mood: int
    description: str | None = None
    date_of_entry: date = Field(default_factory=date.today)
    type: SkillType = SkillType.DBT

    targets: list[DiaryCardTargetReq] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[DiaryCardSkillReq] | None = None


class UpdateDiaryCardReq(BaseModel):
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None

    targets: list[DiaryCardTargetReq] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[DiaryCardSkillReq] | None = None
