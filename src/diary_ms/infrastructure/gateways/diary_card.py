import datetime
import uuid

from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.entities.medicaments import MedicamentDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.value_objects.emotion import EmotionDM
from src.diary_ms.domain.model.value_objects.skill import SkillDM
from src.diary_ms.infrastructure.gateways.base import BaseGateway
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class DiaryCardGateway(BaseGateway[DiaryCard, DiaryCardDM]):
    def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCardDM]:
        return [
            DiaryCardDM(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                description='Some desc.',
                mood=1,
                date_of_entry=datetime.date.today(),
                targets=[TargetDM(id=uuid.uuid4(), user_id=uuid.uuid4(), urge='urge', action='action', ), ],
                emotions=[EmotionDM(id=uuid.uuid4(), name='Anger')],
                medicaments=[MedicamentDM(id=uuid.uuid4(), )],
                skills=[SkillDM(id=uuid.uuid4(), group='group', category='category', name='name')],
            )
        ]
