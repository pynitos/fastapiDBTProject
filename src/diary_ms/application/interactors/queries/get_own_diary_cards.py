from src.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from src.diary_ms.application.interfaces.gateway import ReaderProtocol
from src.diary_ms.application.interfaces.id_provider import IdProvider
from src.diary_ms.application.interfaces.interactor import Interactor
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM


class GetOwnDiaryCards(Interactor[GetOwnDiaryCardsDTO, list[DiaryCardDM]]):
    def __init__(
            self,
            db_gateway: ReaderProtocol,
            id_provider: IdProvider
    ):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, query: GetOwnDiaryCardsDTO) -> list[DiaryCardDM]:
        diary_cards: list[DiaryCardDM] = await self.db_gateway.get_all(offset=query.pagination.offset,
                                                                 limit=query.pagination.limit)
        return diary_cards
