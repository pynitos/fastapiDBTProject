import datetime
from uuid import UUID

from sqlmodel import Field

from src.diary_ms.infrastructure.gateways.models.base import Base
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
from src.diary_ms.infrastructure.gateways.models.skill import Skill
from src.diary_ms.infrastructure.gateways.models.target import Target


class DiaryCard(Base, table=True):
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: datetime.date = Field(default_factory=datetime.date.today)
    targets: list[Target] | None = None
    emotions: list[Emotion] | None = None
    medicaments: list[Medicament] | None = None
    skills: list[Skill] | None = None
