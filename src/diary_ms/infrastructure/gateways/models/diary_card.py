import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from src.diary_ms.infrastructure.gateways.models.base import Base

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
    from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
    from src.diary_ms.infrastructure.gateways.models.skill import Skill
    from src.diary_ms.infrastructure.gateways.models.target import Target


class DiaryCardSkillLink(SQLModel, table=True):
    diary_card_id: UUID | None = Field(
        default=None, foreign_key="diarycard.id", primary_key=True
    )
    skill_id: UUID | None = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )


class DiaryCardTargetLink(SQLModel, table=True):
    diary_card_id: UUID | None = Field(
        default=None, foreign_key="diarycard.id", primary_key=True
    )
    skill_id: UUID | None = Field(
        default=None, foreign_key="target.id", primary_key=True
    )


class DiaryCardEmotionLink(SQLModel, table=True):
    diary_card_id: UUID | None = Field(
        default=None, foreign_key="diarycard.id", primary_key=True
    )
    skill_id: UUID | None = Field(
        default=None, foreign_key="emotion.id", primary_key=True
    )


class DiaryCardMedicamentLink(SQLModel, table=True):
    diary_card_id: UUID | None = Field(
        default=None, foreign_key="diarycard.id", primary_key=True
    )
    skill_id: UUID | None = Field(
        default=None, foreign_key="medicament.id", primary_key=True
    )


class DiaryCard(Base, table=True):
    user_id: UUID
    mood: int
    description: str | None = None
    date_of_entry: datetime.date = Field(default_factory=datetime.date.today)
    targets: list["Target"] | None = Relationship(
        back_populates="diary_cards",
        link_model=DiaryCardTargetLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    emotions: list["Emotion"] | None = Relationship(
        back_populates="diary_cards",
        link_model=DiaryCardEmotionLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    medicaments: list["Medicament"] | None = Relationship(
        back_populates="diary_cards",
        link_model=DiaryCardMedicamentLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    skills: list["Skill"] | None = Relationship(
        back_populates="diary_cards",
        link_model=DiaryCardSkillLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
