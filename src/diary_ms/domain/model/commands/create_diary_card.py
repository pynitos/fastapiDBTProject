from dataclasses import dataclass, field
from datetime import date

from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.commands.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.commands.create_skill import CreateSkillCommand
from src.diary_ms.domain.model.commands.create_target import CreateTargetCommand
from src.diary_ms.domain.model.entities.user_id import UserId


@dataclass
class CreateDiaryCardCommand:
    user_id: UserId
    mood: int

    id: DiaryCardId | None = None
    description: str | None = None
    date_of_entry: date = field(default_factory=date.today)

    targets: list[CreateTargetCommand] | None = None
    emotions: list[CreateEmotionCommand] | None = None
    medicaments: list[CreateMedicamentCommand] | None = None
    skills: list[CreateSkillCommand] | None = None
