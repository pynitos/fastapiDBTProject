from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardsDTO,
    OwnDiaryCardDTO,
)
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from src.diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.entities.user_id import UserId


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
        user_id: UserId = self._id_provider.get_current_user_id()
        diary_cards: list[DiaryCard] = await self._db_gateway.get_all(
            user_id=user_id, offset=query.pagination.offset, limit=query.pagination.limit
        )
        dtos: list[OwnDiaryCardDTO] = self._mapper.dm_list_to_dto_list(diary_cards)
        return dtos
