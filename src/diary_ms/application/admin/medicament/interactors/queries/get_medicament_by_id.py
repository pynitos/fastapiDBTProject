from src.diary_ms.application.admin.medicament.dto.mappers.medicament import MedicamentAdminDTOMapper
from src.diary_ms.application.admin.medicament.dto.medicament import GetMedicamentAdminDTO, MedicamentAdminDTO
from src.diary_ms.application.admin.medicament.exceptions.medicament import MedicamentNotFoundAdminError
from src.diary_ms.application.admin.medicament.interfaces.gateway import MedicamentAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class GetMedicamentAdminHandler(QueryHandler[GetMedicamentAdminDTO, MedicamentAdminDTO]):
    def __init__(self, db_gateway: MedicamentAdminReader, id_provider: AdminIdProvider):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper: type[MedicamentAdminDTOMapper] = MedicamentAdminDTOMapper

    async def __call__(self, query: GetMedicamentAdminDTO) -> MedicamentAdminDTO:
        self._id_provider.get_admin_user_id()
        med_id: MedicamentId = MedicamentId(query.id)
        med: Medicament | None = await self._db_gateway.get_by_id(med_id)
        if not med:
            raise MedicamentNotFoundAdminError(med_id)
        return self._mapper.dm_to_dto(med)
