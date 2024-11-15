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
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
from src.diary_ms.infrastructure.gateways.models.skill import Skill
from src.diary_ms.infrastructure.gateways.models.target import Target


class DiaryCardGateway(BaseGateway[DiaryCard, DiaryCardDM]):
    def create(self, entity: DiaryCardDM) -> None:
        db_entity: DiaryCard = DiaryCard(
            user_id=entity.user_id,
            mood=entity.mood,
            description=entity.description,
            date_of_entry=entity.date_of_entry,
            targets=[Target(user_id=entity.user_id, urge=x.urge, action=x.action) for x in entity.targets],
            emotions=[Emotion(name=x.name, description=x.description) for x in entity.emotions],
            medicaments=[Medicament(user_id=entity.user_id, name=x.name, dosage=x.dosage) for x in entity.medicaments],
            skills=[Skill(category=x.category, group=x.group, name=x.name, type=x.type) for x in entity.skills],
        )
        self._session.add(db_entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCardDM]:
        return await super().get_all(offset, limit)
