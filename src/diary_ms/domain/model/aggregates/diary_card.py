from dataclasses import dataclass, field
from typing import Self
from uuid import UUID

from src.diary_ms.domain.common.exceptions.base import DomainError
from src.diary_ms.domain.common.model.aggregates.base import AggregateRoot
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.coping_strategy import CopingStrategy
from src.diary_ms.domain.model.entities.diary_card_skill import SkillUsage
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import (
    DCDateOfEntry,
)
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class DiaryCard(AggregateRoot):
    user_id: UserId
    mood: DCMood
    id: DiaryCardId = DiaryCardId(None)
    description: DCDescription = DCDescription(value=None)
    date_of_entry: DCDateOfEntry = DCDateOfEntry()
    emotions: list[Emotion] = field(default_factory=list)
    targets: list[Target] = field(default_factory=list)
    medicaments: list[Medicament] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    type: SkillType = SkillType.DBT

    coping_strategies: list[CopingStrategy] = field(default_factory=list)
    emotions_ids: list[UUID] | None = None
    medicaments_ids: list[UUID] | None = None
    skill_usages: list[SkillUsage] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        mood: DCMood,
        id: DiaryCardId,
        user_id: UserId,
        description: DCDescription,
        date_of_entry: DCDateOfEntry,
        targets: list[CopingStrategy] | None = None,
        emotions: list[UUID] | None = None,
        medicaments: list[UUID] | None = None,
        skills: list[SkillUsage] | None = None,
        skill_type: SkillType = SkillType.DBT,
    ) -> Self:
        if not id.value:
            raise DomainError
        diary_card: Self = cls(
            id=id,
            user_id=user_id,
            mood=mood,
            description=description,
            date_of_entry=date_of_entry,
            coping_strategies=targets if targets else [],
            emotions_ids=emotions,
            medicaments_ids=medicaments,
            skill_usages=skills if skills else [],
            type=skill_type,
        )
        diary_card.record_event(
            DiaryCardCreatedEvent(
                diary_card_id=id.value,
                user_id=diary_card.user_id.value,
                date_of_entry=diary_card.date_of_entry.value,
                type=diary_card.type.value,
            )
        )
        return diary_card

    def update(
        self,
        mood: DCMood | None = None,
        description: DCDescription | None = None,
        date_of_entry: DCDateOfEntry | None = None,
        targets: list[CopingStrategy] | None = None,
        emotions: list[UUID] | None = None,
        medicaments: list[UUID] | None = None,
        skills: list[SkillUsage] | None = None,
        skill_type: SkillType | None = SkillType.DBT,
    ) -> Self:
        if mood:
            self.mood = mood
        if description:
            self.description = description
        if date_of_entry:
            self.date_of_entry = date_of_entry
        if targets:
            self.coping_strategies = targets
        if emotions:
            self.emotions_ids = emotions
        if medicaments:
            self.medicaments_ids = medicaments
        if skills:
            self.skill_usages = skills
        if skill_type:
            self.type = skill_type

        return self
