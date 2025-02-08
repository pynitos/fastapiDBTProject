from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.admin.target_behavior.interfaces.gateway import (
    TargetAdminDeleter,
    TargetAdminReader,
    TargetAdminSaver,
    TargetAdminUpdater,
)
from src.diary_ms.application.target_behavior.exceptions.target_behavior import (
    TargetIdNotProvidedError,
    TargetNotFoundError,
)
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class TargetAdminGateway(
    TargetAdminReader,
    TargetAdminSaver,
    TargetAdminUpdater,
    TargetAdminDeleter,
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._db_model: type[Target] = Target

    async def create(self, entity: Target) -> None:
        self._session.add(entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Target]:
        stmt: Select[tuple[Target]] = select(self._db_model).offset(offset).limit(limit)
        result: ScalarResult[Target] = await self._session.scalars(stmt)
        result_list: list[Target] = list(result.all())
        return result_list

    async def get_by_id(self, id: TargetId) -> Target | None:
        if not id.value:
            raise TargetIdNotProvidedError
        pk: str = str(id.value)
        entity: Target | None = await self._session.get(self._db_model, pk)
        return entity

    async def update(self, entity: Target) -> None:
        self._session.add(entity)

    async def delete(self, id: TargetId) -> None:
        entity: Target | None = await self.get_by_id(id)
        if not entity:
            raise TargetNotFoundError(id)
        await self._session.delete(entity)
