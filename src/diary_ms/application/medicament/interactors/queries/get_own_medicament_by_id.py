from diary_ms.application.common.interfaces.handlers.query import QueryHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.medicament.dto.mappers.medicament import MedicamentDTOMapper
from diary_ms.application.medicament.dto.medicament import GetOwnMedicamentDTO, OwnMedicamentDTO
from diary_ms.application.medicament.exceptions.medicament import MedicamentNotFoundError
from diary_ms.application.medicament.interfaces.gateway import MedicamentReader
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class GetOwnMedicament(QueryHandler[GetOwnMedicamentDTO, OwnMedicamentDTO]):
    def __init__(self, db_gateway: MedicamentReader, id_provider: IdProvider):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper: type[MedicamentDTOMapper] = MedicamentDTOMapper

    async def __call__(self, query: GetOwnMedicamentDTO) -> OwnMedicamentDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        med_id: MedicamentId = MedicamentId(query.id)
        med: Medicament | None = await self._db_gateway.get_by_id(med_id, user_id)
        if not med:
            raise MedicamentNotFoundError(med_id)
        return self._mapper.dm_to_dto(med)
