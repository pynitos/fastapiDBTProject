import uuid
from dataclasses import dataclass, field
from typing import Any

from diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from diary_ms.domain.model.value_objects.skill.effectiveness import SkillEffectiveness
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.id import CopingStrategyId
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.intensity import UrgeIntensity
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId


@dataclass
class CopingStrategy:
    target_id: TargetId
    diary_card_id: DiaryCardId
    id: CopingStrategyId = field(default_factory=lambda: CopingStrategyId(uuid.uuid4()))
    action: CopingAction | None = None
    effectiveness: SkillEffectiveness | None = None
    urge_intensity: UrgeIntensity | None = None

    @classmethod
    def create(
        cls,
        target_id: TargetId,
        diary_card_id: DiaryCardId,
        action: CopingAction | None = None,
        effectiveness: SkillEffectiveness | None = None,
        urge_intensity: UrgeIntensity | None = None,
    ) -> "CopingStrategy":
        """Фабричный метод с валидацией"""
        return cls(
            target_id=target_id,
            diary_card_id=diary_card_id,
            action=action,
            effectiveness=effectiveness,
            urge_intensity=urge_intensity,
        )

    def has_urge(self) -> bool:
        return self.urge_intensity is not None and not self.urge_intensity.is_absent()

    def is_effective(self) -> bool:
        return self.effectiveness is not None and self.effectiveness.is_effective()

    def get_summary(self) -> dict[str, Any]:
        return {
            "action": self.action.value if self.action else None,
            "effectiveness": self.effectiveness.value if self.effectiveness else None,
            "urge_intensity": {
                "value": self.urge_intensity.value if self.urge_intensity else None,
                "description": self.urge_intensity.describe() if self.urge_intensity else None,
            },
            "is_urgent": self.has_urge() and self.urge_intensity.is_strong() if self.urge_intensity else None,
        }
