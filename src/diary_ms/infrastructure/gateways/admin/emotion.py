from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.admin.emotion.interfaces.gateway import AdminEmotionSaver
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.infrastructure.gateways.admin.mappers.emotion import EmotionMapper
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion


class AdminEmotionGateway(AdminEmotionSaver):
    def __init__(
        self,
        db_model: type[Emotion],
        domain_model: type[EmotionDM],
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._db_model = db_model
        self._domain_model = domain_model
        self._mapper: type[EmotionMapper] = EmotionMapper

    async def create(self, entity: EmotionDM) -> None:
        raise NotImplementedError
