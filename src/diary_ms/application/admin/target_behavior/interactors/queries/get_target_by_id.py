from src.diary_ms.application.admin.target_behavior.dto.mappers.target_behavior import TargetAdminDTOMapper
from src.diary_ms.application.admin.target_behavior.dto.target_behavior import GetTargetAdminDTO, TargetAdminDTO
from src.diary_ms.application.admin.target_behavior.exceptions.target_behavior import TargetNotFoundAdminError
from src.diary_ms.application.admin.target_behavior.interfaces.gateway import TargetAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class GetTargetAdminHandler(QueryHandler[GetTargetAdminDTO, TargetAdminDTO]):
    def __init__(self, db_gateway: TargetAdminReader, id_provider: AdminIdProvider) -> None:
        self._db_gateway: TargetAdminReader = db_gateway
        self._id_provider: AdminIdProvider = id_provider
        self._mapper: type[TargetAdminDTOMapper] = TargetAdminDTOMapper

    async def __call__(self, query: GetTargetAdminDTO) -> TargetAdminDTO:
        self._id_provider.get_admin_user_id()
        target_id: TargetId = TargetId(query.id)
        med: Target | None = await self._db_gateway.get_by_id(target_id)
        if not med:
            raise TargetNotFoundAdminError(target_id)
        return self._mapper.dm_to_dto(med)
