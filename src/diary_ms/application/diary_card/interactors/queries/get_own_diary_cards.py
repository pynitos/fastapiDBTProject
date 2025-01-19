from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.diary_card import (
    GetOwnDiaryCardsDTO,
    OwnDiaryCardDTO,
)
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader


class GetOwnDiaryCards(QueryHandler[GetOwnDiaryCardsDTO, list[OwnDiaryCardDTO]]):
    def __init__(self, db_gateway: DiaryCardReader, id_provider: IdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, query: GetOwnDiaryCardsDTO) -> list[OwnDiaryCardDTO]:
        diary_cards: list[OwnDiaryCardDTO] = await self.db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )
        dtos: list[OwnDiaryCardDTO] = [
            OwnDiaryCardDTO(
                id=x.id.value,
                user_id=x.id.value,
                mood=x.mood.value,
                description=x.description.value,
                date_of_entry=x.date_of_entry.value,
                type=x.type.value,
                targets=[],
                emotions=[],
                medicaments=[],
                skills=[],
            )
            for x in diary_cards
        ]

        return dtos
