from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.medicament.dto.mappers.medicament import MedicamentDTOMapper
from src.diary_ms.application.medicament.dto.medicament import GetOwnMedicamentsDTO, OwnMedicamentDTO
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentReader
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.user_id import UserId


class GetOwnMedicaments(QueryHandler[GetOwnMedicamentsDTO, list[OwnMedicamentDTO]]):
    def __init__(
        self,
        db_gateway: MedicamentReader,
        id_provider: IdProvider,
    ) -> None:
        self._db_gateway: MedicamentReader = db_gateway
        self._id_provider: IdProvider = id_provider
        self._mapper: type[MedicamentDTOMapper] = MedicamentDTOMapper

    async def __call__(self, query: GetOwnMedicamentsDTO) -> list[OwnMedicamentDTO]:
        user_id: UserId = self._id_provider.get_current_user_id()
        meds: list[Medicament] = await self._db_gateway.get_all(
            user_id=user_id,
            offset=query.pagination.offset,
            limit=query.pagination.limit,
        )
        dtos: list[OwnMedicamentDTO] = self._mapper.dm_list_to_dto_list(meds)
        return dtos
