from dataclasses import dataclass

from diary_ms.application.common.dto.base import ResultDTO
from diary_ms.application.common.dto.query import Query
from diary_ms.application.diary_card.dto.diary_card import EmotionResultDTO
from diary_ms.application.diary_card.dto.skill import SkillDTO
from diary_ms.application.medicament.dto.medicament import OwnMedicamentDTO
from diary_ms.application.target_behavior.dto.target_behavior import OwnTargetResultDTO
from diary_ms.domain.model.value_objects.skill.type import SkillType


@dataclass
class DataForDiaryCardDTO(ResultDTO):
    emotions: list[EmotionResultDTO]
    skills: list[SkillDTO]
    targets: list[OwnTargetResultDTO]
    medicaments: list[OwnMedicamentDTO]


@dataclass
class GetDataForDiaryCardQuery(Query[DataForDiaryCardDTO]):
    skill_type: SkillType = SkillType.DBT
