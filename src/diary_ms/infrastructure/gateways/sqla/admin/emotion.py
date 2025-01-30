from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.admin.emotion.interfaces.gateway import (
    EmotionAdminDeleter,
    EmotionAdminReader,
    EmotionAdminSaver,
    EmotionAdminUpdater,
)
from src.diary_ms.application.common.exceptions.base import GatewayError
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


class EmotionAdminGateway(EmotionAdminSaver, EmotionAdminReader, EmotionAdminDeleter, EmotionAdminUpdater):
    def __init__(
        self,
        db_model: type[Emotion],
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._db_model = db_model

    async def create(self, entity: Emotion) -> None:
        self._session.add(entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Emotion]:
        stmt: Select[tuple[Emotion]] = select(self._db_model).offset(offset).limit(limit)
        result: ScalarResult[Emotion] = await self._session.scalars(stmt)
        result_list: list[Emotion] = list(result.all())
        return result_list

    async def get_by_id(self, id: EmotionId) -> Emotion | None:
        pk: UUID | None = id.value
        if not pk:
            raise GatewayError("Emotion id not provided!", 400)
        return await self._session.get(self._db_model, pk)

    async def update(self, entity: Emotion) -> None:
        self._session.add(entity)

    async def delete(self, id: EmotionId) -> None:
        entity: Emotion | None = await self.get_by_id(id)
        if not entity:
            raise GatewayError("Emotion for delete not found!", 404)
        await self._session.delete(entity)
