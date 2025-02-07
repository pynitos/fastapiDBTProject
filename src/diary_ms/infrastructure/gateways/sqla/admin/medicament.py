from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.diary_ms.application.admin.medicament.exceptions.medicament import (
    MedicamentIdNotProvidedAdminError,
    MedicamentNotFoundAdminError,
)
from src.diary_ms.application.admin.medicament.interfaces.gateway import (
    MedicamentAdminDeleter,
    MedicamentAdminReader,
    MedicamentAdminSaver,
    MedicamentAdminUpdater,
)
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class MedicamentAdminGateway(
    MedicamentAdminReader, MedicamentAdminSaver, MedicamentAdminUpdater, MedicamentAdminDeleter
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._db_model: type[Medicament] = Medicament

    async def create(self, entity: Medicament) -> None:
        self._session.add(entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Medicament]:
        stmt: Select[tuple[Medicament]] = select(self._db_model).offset(offset).limit(limit)
        result: ScalarResult[Medicament] = await self._session.scalars(stmt)
        result_list: list[Medicament] = list(result.all())
        return result_list

    async def get_by_id(self, id: MedicamentId) -> Medicament | None:
        if not id.value:
            raise MedicamentIdNotProvidedAdminError
        pk: str = str(id.value)
        entity: Medicament | None = await self._session.get(self._db_model, pk)
        return entity

    async def update(self, entity: Medicament) -> None:
        self._session.add(entity)

    async def delete(self, id: MedicamentId) -> None:
        entity: Medicament | None = await self.get_by_id(id)
        if not entity:
            raise MedicamentNotFoundAdminError(id)
        await self._session.delete(entity)
