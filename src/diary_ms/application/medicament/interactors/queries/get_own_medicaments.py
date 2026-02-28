from diary_ms.application.common.interfaces.handlers.query import QueryHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.medicament.dto.mappers.medicament import MedicamentDTOMapper
from diary_ms.application.medicament.dto.medicament import GetOwnMedicamentsDTO, OwnMedicamentDTO, OwnMedicamentsDTO
from diary_ms.application.medicament.interfaces.gateway import MedicamentReader
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.user_id import UserId


class GetOwnMedicaments(QueryHandler[GetOwnMedicamentsDTO, OwnMedicamentsDTO]):
    def __init__(
        self,
        db_gateway: MedicamentReader,
        id_provider: IdProvider,
    ) -> None:
        self._db_gateway: MedicamentReader = db_gateway
        self._id_provider: IdProvider = id_provider
        self._mapper: type[MedicamentDTOMapper] = MedicamentDTOMapper

    async def __call__(self, query: GetOwnMedicamentsDTO) -> OwnMedicamentsDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        total: int = await self._db_gateway.get_total_count(user_id)
        if total == 0:
            return OwnMedicamentsDTO()
        meds: list[Medicament] = await self._db_gateway.get_all(
            user_id=user_id,
            offset=query.pagination.offset,
            limit=query.pagination.limit,
        )
        dtos: list[OwnMedicamentDTO] = self._mapper.dm_list_to_dto_list(meds)
        return OwnMedicamentsDTO(dtos, total)
