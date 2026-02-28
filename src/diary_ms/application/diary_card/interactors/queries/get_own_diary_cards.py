from diary_ms.application.common.interfaces.handlers.query import QueryHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardsQuery,
    OwnDiaryCardResultDTO,
    OwnDiaryCardsResultDTO,
)
from diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper
from diary_ms.domain.model.aggregates.diary_card import DiaryCard
from diary_ms.domain.model.entities.user_id import UserId


class GetOwnDiaryCards(QueryHandler[GetOwnDiaryCardsQuery, OwnDiaryCardsResultDTO]):
    def __init__(
        self,
        db_gateway: DiaryCardReader,
        id_provider: IdProvider,
        mapper: DiaryCardDTOMapper,
    ):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetOwnDiaryCardsQuery) -> OwnDiaryCardsResultDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        total: int = await self._db_gateway.get_total_count(user_id)
        diary_cards: list[DiaryCard] = await self._db_gateway.get_all(
            user_id=user_id, offset=query.pagination.offset, limit=query.pagination.limit
        )
        diary_cards_dtos: list[OwnDiaryCardResultDTO] = self._mapper.dm_list_to_dto_list(diary_cards)
        return OwnDiaryCardsResultDTO(diary_cards=diary_cards_dtos, total=total)
