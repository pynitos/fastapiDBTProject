from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.diary_card import GetOwnDiaryCardDTO, OwnDiaryCardDTO
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from src.diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetOwnDiaryCard(QueryHandler[GetOwnDiaryCardDTO, OwnDiaryCardDTO | None]):
    def __init__(self, db_gateway: DiaryCardReader, id_provider: IdProvider, mapper: DiaryCardDTOMapper):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetOwnDiaryCardDTO) -> OwnDiaryCardDTO | None:
        diary_card: DiaryCard | None = await self._db_gateway.get_by_id(DiaryCardId(query.id))
        return self._mapper.dm_to_dto(diary_card) if diary_card else None
