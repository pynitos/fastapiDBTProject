from datetime import date
from dataclasses import dataclass, field

from src.diary_ms.domain.common.model.aggregates.base import AggregateRoot
from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicaments import Medicament
from src.diary_ms.domain.model.value_objects.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM


@dataclass
class DiaryCardDM(AggregateRoot):
    id: DiaryCardId
    user_id: UserId

    mood: int
    description: str | None = None
    date: date = field(default_factory=date.today)

    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[Medicament] | None = None

    skills: list[SkillDM] | None = None

