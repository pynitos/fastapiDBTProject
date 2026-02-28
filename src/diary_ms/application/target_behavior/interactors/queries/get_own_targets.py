from diary_ms.application.common.interfaces.handlers.query import QueryHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.target_behavior.dto.mappers.target_behavior import TargetDTOMapper
from diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnTargetsQuery,
    OwnTargetResultDTO,
    OwnTargetsResultDTO,
)
from diary_ms.application.target_behavior.interfaces.gateway import TargetReader
from diary_ms.domain.model.entities.target_behavior import Target
from diary_ms.domain.model.entities.user_id import UserId


class GetOwnTargets(QueryHandler[GetOwnTargetsQuery, OwnTargetsResultDTO]):
    def __init__(
        self,
        db_gateway: TargetReader,
        id_provider: IdProvider,
    ) -> None:
        self._db_gateway: TargetReader = db_gateway
        self._id_provider: IdProvider = id_provider
        self._mapper: type[TargetDTOMapper] = TargetDTOMapper

    async def __call__(self, query: GetOwnTargetsQuery) -> OwnTargetsResultDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        total: int = await self._db_gateway.get_total_count(user_id)
        if total == 0:
            return OwnTargetsResultDTO()
        targets: list[Target] = await self._db_gateway.get_all_own(
            user_id=user_id,
            offset=query.pagination.offset,
            limit=query.pagination.limit,
        )
        dtos: list[OwnTargetResultDTO] = self._mapper.dm_list_to_dto_list(targets)
        return OwnTargetsResultDTO(targets=dtos, total=total)
