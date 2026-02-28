from sqlalchemy import ScalarResult, Select, Table, func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from diary_ms.application.medicament.exceptions.medicament import (
    MedicamentIdNotProvidedError,
    MedicamentNotFoundError,
)
from diary_ms.application.medicament.interfaces.gateway import (
    MedicamentDeleter,
    MedicamentReader,
    MedicamentSaver,
    MedicamentUpdater,
)
from diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.medicament.id import MedicamentId

from .db.tables import medicaments_table


class MedicamentGateway(MedicamentReader, MedicamentSaver, MedicamentUpdater, MedicamentDeleter):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
        self._model: type[Medicament] = Medicament
        self._table: Table = medicaments_table

    async def create(self, entity: Medicament) -> None:
        self._session.add(entity)

    async def get_total_count(self, user_id: UserId) -> int:
        if not user_id.value:
            raise UserIdNotProvidedError
        query: Select[tuple[int]] = (
            select(func.count()).select_from(self._model).where(self._table.c.user_id == user_id.value)
        )
        result: int | None = await self._session.scalar(query)
        return result or 0

    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Medicament]:
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Medicament]] = (
            select(self._model).where(medicaments_table.c.user_id == user_id.value).offset(offset).limit(limit)
        )
        result: ScalarResult[Medicament] = await self._session.scalars(stmt)
        result_list: list[Medicament] = list(result.all())
        return result_list

    async def get_by_id(self, id: MedicamentId, user_id: UserId) -> Medicament | None:
        if not id.value:
            raise MedicamentIdNotProvidedError
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Medicament]] = select(self._model).where(
            self._model.id == id,  # type: ignore
            self._model.user_id == user_id,  # type: ignore
        )
        result: ScalarResult[Medicament] = await self._session.scalars(stmt)
        entity: Medicament | None = result.first()
        return entity

    async def update(self, entity: Medicament) -> None:
        self._session.add(entity)

    async def delete(self, id: MedicamentId, user_id: UserId) -> None:
        entity: Medicament | None = await self.get_by_id(id, user_id)
        if not entity:
            raise MedicamentNotFoundError(id)
        await self._session.delete(entity)
