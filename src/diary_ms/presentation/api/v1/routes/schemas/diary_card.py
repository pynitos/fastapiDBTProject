from datetime import date

from pydantic import BaseModel, Field

from src.diary_ms.domain.model.value_objects.skill.type import SkillType


class CreateTargetReq(BaseModel):
    urge: str
    action: str


class CreateEmotionReq(BaseModel):
    name: str
    description: str = None


class CreateMedicamentReq(BaseModel):
    name: str
    dosage: str


class CreateSkillReq(BaseModel):
    category: str
    group: str
    name: str
    type: SkillType = SkillType.DBT


class CreateDiaryCardReq(BaseModel):
    mood: int
    description: str | None = None
    date_of_entry: date = Field(default_factory=date.today)

    targets: list[CreateTargetReq] | None = None
    emotions: list[CreateEmotionReq] | None = None
    medicaments: list[CreateMedicamentReq] | None = None
    skills: list[CreateSkillReq] | None = None


class UpdateDiaryCardReq(BaseModel):
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None

    targets: list[CreateTargetReq] | None = None
    emotions: list[CreateEmotionReq] | None = None
    medicaments: list[CreateMedicamentReq] | None = None
    skills: list[CreateSkillReq] | None = None
