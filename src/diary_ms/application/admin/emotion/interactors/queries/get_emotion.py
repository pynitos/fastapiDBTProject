from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO, GetEmotionAdminDTO
from src.diary_ms.application.admin.emotion.dto.mapper.emotion import EmotionAdminDTOMapper
from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


class GetEmotionAdminHandler(QueryHandler[GetEmotionAdminDTO, EmotionAdminDTO | None]):
    def __init__(self, db_gateway: EmotionAdminReader, id_provider: IdProvider, mapper: EmotionAdminDTOMapper):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetEmotionAdminDTO) -> EmotionAdminDTO | None:
        emotion: Emotion | None = await self._db_gateway.get_by_id(EmotionId(query.id))
        return self._mapper.dm_to_dto(emotion) if emotion else None
