from src.diary_ms.application.admin.medicament.dto.mappers.medicament import MedicamentAdminDTOMapper
from src.diary_ms.application.admin.medicament.dto.medicament import GetMedicamentsAdminDTO, MedicamentAdminDTO
from src.diary_ms.application.admin.medicament.interfaces.gateway import MedicamentAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.medicament import Medicament


class GetMedicamentsAdminHandler(QueryHandler[GetMedicamentsAdminDTO, list[MedicamentAdminDTO]]):
    def __init__(
        self,
        db_gateway: MedicamentAdminReader,
        id_provider: AdminIdProvider,
    ) -> None:
        self._db_gateway: MedicamentAdminReader = db_gateway
        self._id_provider: AdminIdProvider = id_provider
        self._mapper: type[MedicamentAdminDTOMapper] = MedicamentAdminDTOMapper

    async def __call__(self, query: GetMedicamentsAdminDTO) -> list[MedicamentAdminDTO]:
        self._id_provider.get_admin_user_id()
        meds: list[Medicament] = await self._db_gateway.get_all(
            offset=query.pagination.offset,
            limit=query.pagination.limit,
        )
        return self._mapper.dm_list_to_dto_list(meds)
