from dataclasses import dataclass

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.application.diary_card.dto.diary_card import SkillDTO
from src.diary_ms.application.diary_card.dto.emotion import EmotionDTO
from src.diary_ms.application.medicament.dto.medicament import OwnMedicamentDTO
from src.diary_ms.application.target_behavior.dto.target_behavior import OwnTargetDTO


@dataclass
class DataForDiaryCardDTO(DTO):
    emotions: list[EmotionDTO]
    skills: list[SkillDTO]
    targets: list[OwnTargetDTO]
    medicaments: list[OwnMedicamentDTO]


@dataclass
class GetDataForDiaryCardQuery(Query[DataForDiaryCardDTO]):
    pass
