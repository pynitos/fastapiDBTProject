import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.infrastructure.gateways.db.base import Base
from src.diary_ms.infrastructure.gateways.models.base import BaseMixin

if TYPE_CHECKING:
    from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
    from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
    from src.diary_ms.infrastructure.gateways.models.skill import Skill
    from src.diary_ms.infrastructure.gateways.models.target import Target


class DiaryCardSkill(Base):
    __tablename__ = "diary_card_skill"

    diary_card_id: Mapped[UUID] = mapped_column(
        ForeignKey("diary_cards.id"), primary_key=True
    )
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    description: Mapped[str | None] = mapped_column(default=None)

    skill: Mapped["Skill"] = relationship(lazy="selectin")


class DiaryCardTarget(Base):
    __tablename__ = "diary_card_target"

    diary_card_id: Mapped[UUID] = mapped_column(
        ForeignKey("diary_cards.id"), primary_key=True
    )
    target_id: Mapped[UUID] = mapped_column(ForeignKey("targets.id"), primary_key=True)


class DiaryCardEmotion(Base):
    __tablename__ = "diary_card_emotion"
    diary_card_id: Mapped[UUID] = mapped_column(
        ForeignKey("diary_cards.id"), primary_key=True
    )
    emotion_id: Mapped[UUID] = mapped_column(
        ForeignKey("emotions.id"), primary_key=True
    )


class DiaryCardMedicament(Base):
    __tablename__ = "diary_card_medicament"

    diary_card_id: Mapped[UUID] = mapped_column(
        ForeignKey("diary_cards.id"), primary_key=True
    )
    medicament_id: Mapped[UUID] = mapped_column(
        ForeignKey("medicaments.id"), primary_key=True
    )


class DiaryCard(BaseMixin):
    __tablename__ = "diary_cards"

    user_id: Mapped[UUID]
    mood: Mapped[int]
    description: Mapped[str | None] = mapped_column(String(100))
    date_of_entry: Mapped[datetime.date] = mapped_column(server_default=func.now())

    targets: Mapped[list["Target"]] = relationship(
        secondary="diary_card_target",
        lazy="selectin",
    )
    emotions: Mapped[list["Emotion"]] = relationship(
        secondary="diary_card_emotion", lazy="selectin"
    )
    medicaments: Mapped[list["Medicament"]] = relationship(
        secondary="diary_card_medicament", lazy="selectin"
    )
    skills: Mapped[list["Skill"]] = relationship(
        secondary="diary_card_skill", viewonly=True, lazy="selectin"
    )
    skill_assotiations: Mapped[list["DiaryCardSkill"]] = relationship(lazy="selectin")

    type: Mapped[SkillType] = mapped_column(Enum(SkillType), default=SkillType.DBT)
