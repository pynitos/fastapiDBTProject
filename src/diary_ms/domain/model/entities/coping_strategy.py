import uuid
from dataclasses import dataclass

from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.effectiveness import CopingEffectiveness
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.id import CopingStrategyId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


@dataclass
class CopingStrategy:
    target_id: TargetId
    diary_card_id: DiaryCardId
    action: CopingAction = CopingAction(None)
    id: CopingStrategyId = CopingStrategyId(uuid.uuid4())
    effectiveness: CopingEffectiveness = CopingEffectiveness(None)

    def update_action(self, new_action: str) -> None:
        self.action = CopingAction(new_action)

    def mark_as_effective(self, score: int) -> None:
        self.effectiveness = CopingEffectiveness(score)
