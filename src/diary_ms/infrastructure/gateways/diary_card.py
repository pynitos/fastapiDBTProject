import datetime
import uuid
from typing import Any

from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.entities.medicaments import MedicamentDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.entities.user import User
from src.diary_ms.domain.model.value_objects.emotion import EmotionDM
from src.diary_ms.domain.model.value_objects.skill import SkillDM
from src.diary_ms.infrastructure.gateways.base import BaseGateway
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class DiaryCardGateway(BaseGateway[DiaryCard, DiaryCardDM]):
    def create(self, entity: DiaryCard) -> None:
        db_entity: DiaryCard = self._db_model.model_validate(entity)
        self._session.add(db_entity)

    def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCardDM]:
        return super().get_all(offset, limit)
