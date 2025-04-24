from sqlalchemy import ScalarResult, Select, func, or_, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.target_behavior.exceptions.target_behavior import (
    TargetIdNotProvidedError,
    TargetNotFoundError,
)
from src.diary_ms.application.target_behavior.interfaces.gateway import (
    TargetDeleter,
    TargetReader,
    TargetSaver,
    TargetUpdater,
)
from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault

from .db.tables import targets_table


class TargetGateway(
    TargetReader,
    TargetSaver,
    TargetUpdater,
    TargetDeleter,
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._db_model: type[Target] = Target

    async def create(self, entity: Target) -> None:
        self._session.add(entity)

    async def get_total_count(self, user_id: UserId) -> int:
        if not user_id.value:
            raise UserIdNotProvidedError
        query: Select[tuple[int]] = (
            select(func.count()).select_from(Target).where(targets_table.c.user_id == user_id.value)
        )
        result: int | None = await self._session.scalar(query)
        return result or 0

    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Target]:
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Target]] = (
            select(self._db_model)
            .where(
                or_(
                    self._db_model.user_id == user_id,  # type: ignore
                    self._db_model.is_default == TargetIsDefault(True),  # type: ignore
                )
            )
            .offset(offset)
            .limit(limit)
        )
        result: ScalarResult[Target] = await self._session.scalars(stmt)
        result_list: list[Target] = list(result.all())
        return result_list

    async def get_all_own(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Target]:
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Target]] = (
            select(self._db_model)
            .where(
                self._db_model.user_id == user_id,  # type: ignore
            )
            .offset(offset)
            .limit(limit)
        )
        result: ScalarResult[Target] = await self._session.scalars(stmt)
        result_list: list[Target] = list(result.all())
        return result_list

    async def get_by_id(self, id: TargetId, user_id: UserId) -> Target | None:
        if not id.value:
            raise TargetIdNotProvidedError
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Target]] = select(self._db_model).where(
            self._db_model.id == id,  # type: ignore
            or_(
                self._db_model.is_default == TargetIsDefault(True),  # type: ignore
                self._db_model.user_id == user_id,  # type: ignore
            ),
        )
        result: ScalarResult[Target] = await self._session.scalars(stmt)
        entity: Target | None = result.first()
        return entity

    async def get_own_by_id(self, id: TargetId, user_id: UserId) -> Target | None:
        if not id.value:
            raise TargetIdNotProvidedError
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Target]] = select(self._db_model).where(
            self._db_model.id == id,  # type: ignore
            self._db_model.user_id == user_id,  # type: ignore
        )
        result: ScalarResult[Target] = await self._session.scalars(stmt)
        entity: Target | None = result.first()
        return entity

    async def update(self, entity: Target) -> None:
        self._session.add(entity)

    async def delete(self, id: TargetId, user_id: UserId) -> None:
        entity: Target | None = await self.get_own_by_id(id, user_id)
        if not entity:
            raise TargetNotFoundError(id)
        await self._session.delete(entity)
