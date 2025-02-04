from uuid import UUID

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.medicament.exceptions.medicament import (
    MedicamentIdNotProvidedError,
    MedicamentNotFoundError,
)
from src.diary_ms.application.medicament.interfaces.gateway import (
    MedicamentDeleter,
    MedicamentReader,
    MedicamentSaver,
    MedicamentUpdater,
)
from src.diary_ms.domain.common.exceptions.user_id_not_provided import UserIdNotProvidedError
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class MedicamentGateway(MedicamentReader, MedicamentSaver, MedicamentUpdater, MedicamentDeleter):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._db_model: type[Medicament] = Medicament

    async def create(self, entity: Medicament) -> None:
        self._session.add(entity)

    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Medicament]:
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Medicament]] = (
            select(self._db_model)
            .where(
                self.db.model.user_id == user_id.value  # type: ignore
            )
            .offset(offset)
            .limit(limit)
        )
        result: ScalarResult[Medicament] = await self._session.scalars(stmt)
        result_list: list[Medicament] = list(result.all())
        return result_list

    async def get_by_id(self, id: MedicamentId, user_id: UserId) -> Medicament | None:
        pk: UUID | None = id.value
        if not pk:
            raise MedicamentIdNotProvidedError
        if not user_id.value:
            raise UserIdNotProvidedError
        stmt: Select[tuple[Medicament]] = select(self._db_model).where(
            self._db_model.id == pk,  # type: ignore
            self._db_model.user_id == user_id.value,  # type: ignore
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
