from dataclasses import dataclass

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.application.diary_card.dto.diary_card import EmotionResultDTO
from src.diary_ms.application.diary_card.dto.skill import SkillDTO
from src.diary_ms.application.medicament.dto.medicament import OwnMedicamentDTO
from src.diary_ms.application.target_behavior.dto.target_behavior import OwnTargetResultDTO
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class DataForDiaryCardDTO(ResultDTO):
    emotions: list[EmotionResultDTO]
    skills: list[SkillDTO]
    targets: list[OwnTargetResultDTO]
    medicaments: list[OwnMedicamentDTO]


@dataclass
class GetDataForDiaryCardQuery(Query[DataForDiaryCardDTO]):
    skill_type: SkillType = SkillType.DBT
