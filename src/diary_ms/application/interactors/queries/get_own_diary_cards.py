from src.diary_ms.application.common.interfaces.gateway import ReaderProtocol
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.dto.diary_card import (
    GetOwnDiaryCardsDTO,
    OwnDiaryCardDTO,
)


class GetOwnDiaryCards(Interactor[GetOwnDiaryCardsDTO, list[OwnDiaryCardDTO]]):
    def __init__(self, db_gateway: ReaderProtocol, id_provider: IdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, query: GetOwnDiaryCardsDTO) -> list[OwnDiaryCardDTO]:
        diary_cards: list[OwnDiaryCardDTO] = await self.db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )

        return diary_cards
