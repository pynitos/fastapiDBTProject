from src.diary_ms.application.admin.emotion.dto.emotion import (
    EmotionAdminDTO,
    GetEmotionsAdminDTO,
)
from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.emotion import Emotion


class GetEmotionsAdminHandler(QueryHandler[GetEmotionsAdminDTO, list[EmotionAdminDTO]]):
    def __init__(self, db_gateway: EmotionAdminReader, id_provider: AdminIdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, query: GetEmotionsAdminDTO) -> list[EmotionAdminDTO]:
        self.id_provider.get_admin_user_id()
        emotions: list[Emotion] = await self.db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )

        return emotions
