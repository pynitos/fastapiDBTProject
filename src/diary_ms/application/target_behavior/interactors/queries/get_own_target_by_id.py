from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.target_behavior.dto.mappers.target_behavior import TargetDTOMapper
from src.diary_ms.application.target_behavior.dto.target_behavior import GetOwnTargetQuery, OwnTargetResultDTO
from src.diary_ms.application.target_behavior.exceptions.target_behavior import TargetNotFoundError
from src.diary_ms.application.target_behavior.interfaces.gateway import TargetReader
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class GetOwnTarget(QueryHandler[GetOwnTargetQuery, OwnTargetResultDTO]):
    def __init__(self, db_gateway: TargetReader, id_provider: IdProvider):
        self._db_gateway: TargetReader = db_gateway
        self._id_provider: IdProvider = id_provider
        self._mapper: type[TargetDTOMapper] = TargetDTOMapper

    async def __call__(self, query: GetOwnTargetQuery) -> OwnTargetResultDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        med_id: TargetId = TargetId(query.id)
        med: Target | None = await self._db_gateway.get_by_id(med_id, user_id)
        if not med:
            raise TargetNotFoundError(med_id)
        return self._mapper.dm_to_dto(med)
