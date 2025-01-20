from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardsDTO,
    OwnDiaryCardDTO,
)
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from src.diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper


class GetOwnDiaryCards(QueryHandler[GetOwnDiaryCardsDTO, list[OwnDiaryCardDTO]]):
    def __init__(
        self,
        db_gateway: DiaryCardReader,
        id_provider: IdProvider,
        mapper: DiaryCardDTOMapper,
    ):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetOwnDiaryCardsDTO) -> list[OwnDiaryCardDTO]:
        diary_cards: list[OwnDiaryCardDTO] = await self._db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )
        dtos: list[OwnDiaryCardDTO] = self._mapper.dm_list_to_dto_list(diary_cards)
        return dtos
