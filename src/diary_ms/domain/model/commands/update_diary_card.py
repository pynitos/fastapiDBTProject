from dataclasses import dataclass, field
from datetime import date

from src.diary_ms.domain.model.entities.medicaments import MedicamentDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.value_objects.emotion import EmotionDM
from src.diary_ms.domain.model.value_objects.skill import SkillDM


@dataclass
class UpdateDiaryCardCommand:
    mood: int | None = None
    description: str | None = None
    date: date = field(default_factory=date.today)
    targets: list[TargetDM] | None = None
    emotions: list[EmotionDM] | None = None
    medicaments: list[MedicamentDM] | None = None
    skills: list[SkillDM] | None = None
