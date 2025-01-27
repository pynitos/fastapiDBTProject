from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.diary_ms.domain.common.exceptions.user_id_not_provided import (
    UserIdNotProvidedError,
)
from src.diary_ms.domain.common.model.aggregates.base import AggregateRoot
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.entities.diary_card_skill import DiaryCardSkillAssotiation
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
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.situation import SkillSituation
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class DiaryCard(AggregateRoot):
    user_id: UserId
    mood: DCMood
    id: DiaryCardId = DiaryCardId(value=None)
    description: DCDescription = DCDescription(value=None)
    date_of_entry: DCDateOfEntry = DCDateOfEntry()
    targets: list[Target] | None = None
    emotions: list[Emotion] | None = None
    emotions_ids: list[UUID] | None = None
    medicaments: list[Medicament] | None = None
    skills: list[Skill] | None = None
    type: SkillType = SkillType.DBT

    targets_ids: list[UUID] | None = None
    emotions_ids: list[UUID] | None = None
    medicaments_ids: list[UUID] | None = None
    skill_assotiations: list[UUID] | None = None

    @classmethod
    def create(cls, command: CreateDiaryCardCommand) -> Self:
        if not command.user_id:
            raise UserIdNotProvidedError
        id: UUID = uuid4()
        command.id = uuid4()
        targets = command.targets
        emotions = command.emotions
        medicaments = command.medicaments
        skill_assotiations = [
            DiaryCardSkillAssotiation(
                diary_card_id=DiaryCardId(id),
                skill_id=SkillId(s.id),
                situation=SkillSituation(s.situation),
            )
            for s in command.skills
        ]
        diary_card: Self = cls(
            id=DiaryCardId(command.id),
            user_id=UserId(command.user_id),
            mood=DCMood(command.mood),
            description=DCDescription(command.description),
            date_of_entry=DCDateOfEntry(command.date_of_entry),
            targets_ids=targets,
            emotions_ids=emotions,
            medicaments_ids=medicaments,
            skill_assotiations=skill_assotiations,
            targets=[],
            skills=[],
            emotions=[],
            medicaments=[],
        )
        diary_card.record_event(
            DiaryCardCreatedEvent(
                diary_card_id=id,
                user_id=diary_card.user_id.value,
                date_of_entry=diary_card.date_of_entry.value,
                type=diary_card.type.value,
            )
        )
        return diary_card

    def update(self, command: UpdateDiaryCardCommand) -> Self:
        if command.mood:
            self.mood = DCMood(command.mood)
        if command.description:
            self.description = DCDescription(command.description)
        if command.date_of_entry:
            self.date_of_entry = DCDateOfEntry(command.date_of_entry)
        if command.targets:
            self.targets_ids = command.targets
        if command.emotions:
            emotions = command.emotions
            self.emotions_ids = emotions
        if command.medicaments:
            medicaments = command.medicaments
            self.medicaments_ids = medicaments
        if command.skills:
            skills = command.skills
            self.skill_assotiations = skills
        return self
