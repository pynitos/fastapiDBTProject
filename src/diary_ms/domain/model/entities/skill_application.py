from dataclasses import dataclass

from diary_ms.domain.common.model.entities.base import BaseEntity
from diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from diary_ms.domain.model.value_objects.skill.effectiveness import SkillEffectiveness
from diary_ms.domain.model.value_objects.skill.id import SkillId
from diary_ms.domain.model.value_objects.skill.situation import SkillUsage


@dataclass
class SkillApplication(BaseEntity):
    diary_card_id: DiaryCardId
    skill_id: SkillId
    usage: SkillUsage | None = None
    effectiveness: SkillEffectiveness | None = None
