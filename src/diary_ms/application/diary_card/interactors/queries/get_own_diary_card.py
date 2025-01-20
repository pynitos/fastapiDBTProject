from uuid import UUID

from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.diary_card import OwnDiaryCardDTO
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardDTOReader
from src.diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetOwnDiaryCard(QueryHandler[UUID, OwnDiaryCardDTO | None]):
    def __init__(self, db_gateway: DiaryCardDTOReader, id_provider: IdProvider, mapper: type[DiaryCardDTOMapper]):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, id: UUID) -> OwnDiaryCardDTO | None:
        diary_card: OwnDiaryCardDTO | None = await self.db_gateway.get_dto_by_id(DiaryCardId(id))
        return self._mapper.dm_to_dto(diary_card)
