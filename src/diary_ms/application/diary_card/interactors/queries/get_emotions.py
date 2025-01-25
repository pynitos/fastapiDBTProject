import logging

from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.emotion import EmotionDTO, GetEmotionsDTO
from src.diary_ms.application.diary_card.dto.mappers.emotion import EmotionDTOMapper
from src.diary_ms.application.diary_card.interfaces.gateway import EmotionReader
from src.diary_ms.domain.model.entities.emotion import Emotion

logger = logging.getLogger(__name__)


class GetEmotions(QueryHandler[GetEmotionsDTO, list[EmotionDTO]]):
    def __init__(self, db_gateway: EmotionReader, id_provider: IdProvider, mapper: EmotionDTOMapper):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetEmotionsDTO) -> list[EmotionDTO]:
        self._id_provider.get_current_user_id()
        emotions: list[Emotion] = await self._db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )
        logger.debug(emotions)
        dtos = self._mapper.dm_list_to_dto_list(emotions)
        return dtos
