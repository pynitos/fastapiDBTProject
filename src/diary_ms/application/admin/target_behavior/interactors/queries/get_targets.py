from src.diary_ms.application.admin.target_behavior.dto.mappers.target_behavior import TargetAdminDTOMapper
from src.diary_ms.application.admin.target_behavior.dto.target_behavior import GetTargetsAdminDTO, TargetAdminDTO
from src.diary_ms.application.admin.target_behavior.interfaces.gateway import TargetAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.target_behavior import Target


class GetTargetsAdminHandler(QueryHandler[GetTargetsAdminDTO, list[TargetAdminDTO]]):
    def __init__(
        self,
        db_gateway: TargetAdminReader,
        id_provider: AdminIdProvider,
    ) -> None:
        self._db_gateway: TargetAdminReader = db_gateway
        self._id_provider: AdminIdProvider = id_provider
        self._mapper: type[TargetAdminDTOMapper] = TargetAdminDTOMapper

    async def __call__(self, query: GetTargetsAdminDTO) -> list[TargetAdminDTO]:
        self._id_provider.get_admin_user_id()
        targets: list[Target] = await self._db_gateway.get_all(
            offset=query.pagination.offset,
            limit=query.pagination.limit,
        )
        return self._mapper.dm_list_to_dto_list(targets)
