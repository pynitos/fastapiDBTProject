import datetime
from dataclasses import dataclass

from src.diary_ms.domain.common.model.base import BaseDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicaments import Medicament
from src.diary_ms.domain.model.value_objects.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetBehaviorDM


@dataclass
class DiaryCardDM(BaseDM):
    id: DiaryCardId
    user_id: UserId

    date: datetime.date
    mood: int
    description: str | None = None

    targets: list[TargetBehaviorDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[Medicament] | None = None

    skills: list[SkillDM] | None = None

