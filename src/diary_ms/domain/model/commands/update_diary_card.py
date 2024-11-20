from dataclasses import dataclass
from datetime import date

from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicament import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM


@dataclass
class UpdateDiaryCardCommand:
    id: DiaryCardId
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[MedicamentDM] | None = None
    skills: list[SkillDM] | None = None
