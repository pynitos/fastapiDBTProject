from dataclasses import dataclass

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.situation import SkillSituation


@dataclass
class DiaryCardSkillAssotiation(BaseEntity):
    diary_card_id: DiaryCardId
    skill_id: SkillId
    situation: SkillSituation
