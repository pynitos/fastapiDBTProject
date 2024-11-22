import datetime
from dataclasses import dataclass, field
from typing import Self

from src.diary_ms.domain.common.model.aggregates.base import AggregateRoot
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicament import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import (
    DCDateOfEntry,
)
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood


@dataclass
class DiaryCardDM(AggregateRoot):
    id: DiaryCardId | None
    user_id: UserId
    mood: DCMood
    description: DCDescription | None = None
    date_of_entry: DCDateOfEntry = field(default_factory=datetime.date.today)
    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[MedicamentDM] | None = None
    skills: list[SkillDM] | None = None

    @classmethod
    def create(cls, command: CreateDiaryCardCommand) -> Self:
        targets = [TargetDM.create(target) for target in command.targets]
        emotions = [EmotionDM.create(emotion) for emotion in command.emotions]
        medicaments = [MedicamentDM.create(med) for med in command.medicaments]
        skills = [SkillDM.create(skill) for skill in command.skills]
        diary_card: Self = cls(
            id=command.id,
            user_id=command.user_id,
            mood=DCMood(command.mood),
            description=DCDescription(command.description),
            date_of_entry=DCDateOfEntry(command.date_of_entry),
            targets=targets,
            emotions=emotions,
            medicaments=medicaments,
            skills=skills,
        )
        return diary_card

    def update(self, command: UpdateDiaryCardCommand) -> Self:
        if command.mood:
            self.mood = command.mood
        if command.description:
            self.description = command.description
        if command.date_of_entry:
            self.date_of_entry = command.date_of_entry
        if command.targets:
            targets = [TargetDM.create(target) for target in command.targets]
            self.targets = targets
        if command.emotions:
            emotions = [EmotionDM.create(emotion) for emotion in command.emotions]
            self.emotions = emotions
        if command.medicaments:
            medicaments = [MedicamentDM.create(med) for med in command.medicaments]
            self.medicaments = medicaments
        if command.skills:
            skills = [SkillDM.create(skill) for skill in command.skills]
            self.skills = skills
        return self
