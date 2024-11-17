from dataclasses import dataclass, field
from datetime import date

from src.diary_ms.domain.model.entities.medicaments import MedicamentDM

from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM


@dataclass
class UpdateDiaryCardCommand:
    mood: int | None = None
    description: str | None = None
    date_of_entry: date = field(default_factory=date.today)
    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[MedicamentDM] | None = None
    skills: list[SkillDM] | None = None
