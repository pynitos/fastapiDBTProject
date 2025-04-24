from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.target_behavior.dto.mappers.target_behavior import TargetDTOMapper
from src.diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnAndDefaultTargetsQuery,
    OwnTargetResultDTO,
    OwnTargetsResultDTO,
)
from src.diary_ms.application.target_behavior.interfaces.gateway import TargetReader
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId


class GetOwnAndDefaultTargets(QueryHandler[GetOwnAndDefaultTargetsQuery, OwnTargetsResultDTO]):
    def __init__(
        self,
        db_gateway: TargetReader,
        id_provider: IdProvider,
    ) -> None:
        self._db_gateway: TargetReader = db_gateway
        self._id_provider: IdProvider = id_provider
        self._mapper: type[TargetDTOMapper] = TargetDTOMapper

    async def __call__(self, query: GetOwnAndDefaultTargetsQuery) -> OwnTargetsResultDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        total: int = await self._db_gateway.get_total_count(user_id)
        if total == 0:
            return OwnTargetsResultDTO()
        targets: list[Target] = await self._db_gateway.get_all(
            user_id=user_id,
            offset=query.pagination.offset,
            limit=query.pagination.limit,
        )
        dtos: list[OwnTargetResultDTO] = self._mapper.dm_list_to_dto_list(targets)
        return OwnTargetsResultDTO(dtos, total)
