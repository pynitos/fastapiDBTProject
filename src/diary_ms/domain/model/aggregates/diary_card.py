import datetime
from dataclasses import dataclass, field
from typing import Self

from src.diary_ms.domain.common.model.aggregates.base import AggregateRoot
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicaments import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood


@dataclass
class DiaryCardDM(AggregateRoot):
    id: DiaryCardId | None
    user_id: UserId
    mood: DCMood
    description: str | None = None
    date_of_entry: datetime.date = field(default_factory=datetime.date.today)
    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[MedicamentDM] | None = None
    skills: list[SkillDM] | None = None

    @classmethod
    def create(cls, command: CreateDiaryCardCommand) -> Self:
        diary_card: Self = cls(
            id=command.id,
            user_id=command.user_id,
            mood=DCMood(command.mood),
            description=command.description,
            date_of_entry=command.date_of_entry,
            targets=command.targets,
            emotions=command.emotions,
            medicaments=command.medicaments,
            skills=command.skills
        )
        return diary_card

    def update(self, command: UpdateDiaryCardCommand) -> Self:
        if command.mood:
            self.mood = command.mood
        if command.description:
            self.description = command.description
        if command.date:
            self.date_of_entry = command.date
        if command.targets:
            self.targets = command.targets
        if command.emotions:
            self.emotions = command.emotions
        if command.medicaments:
            self.medicaments = command.medicaments
        if command.skills:
            self.skills = command.skills
        return self
