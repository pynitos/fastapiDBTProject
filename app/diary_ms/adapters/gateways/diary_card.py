import datetime
import uuid

from app.diary_ms.adapters.gateways.base import BaseGateway
from app.diary_ms.adapters.models.diary_card import DiaryCard
from app.diary_ms.domain.models.diary_card import DiaryCardDM


class DiaryCardGateway(BaseGateway[DiaryCard, DiaryCardDM]):
    def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCardDM]:
        return [
            DiaryCardDM(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                description='Some desc.',
                updated_at=datetime.datetime.now(datetime.UTC),
                created_at=datetime.datetime.now(datetime.UTC)),
        ]
