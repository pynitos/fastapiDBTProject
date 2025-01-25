import logging

from src.diary_ms.application.admin.emotion.dto.emotion import (
    EmotionAdminDTO,
    GetEmotionsAdminDTO,
)
from src.diary_ms.application.admin.emotion.dto.mapper.emotion import EmotionAdminDTOMapper
from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.emotion import Emotion

logger = logging.getLogger(__name__)


class GetEmotionsAdminHandler(QueryHandler[GetEmotionsAdminDTO, list[EmotionAdminDTO]]):
    def __init__(self, db_gateway: EmotionAdminReader, id_provider: AdminIdProvider, mapper: EmotionAdminDTOMapper):
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetEmotionsAdminDTO) -> list[EmotionAdminDTO]:
        self.id_provider.get_admin_user_id()
        emotions: list[Emotion] = await self.db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )
        logger.debug(emotions)
        dtos = self._mapper.dm_list_to_dto_list(emotions)
        return dtos
