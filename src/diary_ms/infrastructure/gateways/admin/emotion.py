from collections.abc import Sequence

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
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
        db_entity: Emotion = Emotion(
            id=entity.id.value,
            user_id=entity.user_id.value,
            name=entity.name.value,
            description=entity.description.value,
        )
        self._session.add(db_entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[EmotionAdminDTO]:
        stmt: Select[tuple[Emotion]] = (
            select(self._db_model).offset(offset).limit(limit)
        )
        result: ScalarResult[Emotion] = await self._session.scalars(stmt)
        result_list: Sequence[Emotion] = result.all()
        dto_list: list[EmotionAdminDTO] = self._mapper.db_list_to_dto_list(result_list)
        return dto_list
