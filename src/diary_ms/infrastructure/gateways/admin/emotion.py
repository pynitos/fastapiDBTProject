from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
from src.diary_ms.application.admin.emotion.interfaces.gateway import (
    EmotionAdminReader,
    EmotionAdminSaver,
)
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.infrastructure.gateways.admin.converters.emotion import (
    EmotionAdminMapper,
)
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion


class EmotionAdminGateway(EmotionAdminSaver, EmotionAdminReader):  # noqa: F821
    def __init__(
        self,
        db_model: type[Emotion],
        domain_model: type[EmotionDM],
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._db_model = db_model
        self._domain_model = domain_model
        self._mapper: type[EmotionAdminMapper] = EmotionAdminMapper

    async def create(self, entity: EmotionDM) -> None:
        db_entity: Emotion = Emotion(
            id=entity.id.value,
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

    async def get_by_id(self, id: EmotionId) -> EmotionDM | None:
        entity: Emotion | None = await self._get_by_id(pk=id.value)
        if not entity:
            return None
        return self._mapper.db_to_dm(entity)
    
    async def _get_by_id(self, pk: UUID | None) -> Emotion | None:
        if not pk:
            return None
        return await self._session.get(self._db_model, pk)
