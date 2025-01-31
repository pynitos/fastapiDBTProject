from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    DiaryCardForUpdateDTO,
    GetDiaryCardForUpdateDTO,
)
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDTOForUpdateReader,
)
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetDiaryCardForUpdate(QueryHandler[GetDiaryCardForUpdateDTO, DiaryCardForUpdateDTO | None]):
    def __init__(self, db_gateway: DiaryCardDTOForUpdateReader, id_provider: IdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, query: GetDiaryCardForUpdateDTO) -> DiaryCardForUpdateDTO | None:
        dto: DiaryCardForUpdateDTO | None = await self.db_gateway.get_dto_for_update(DiaryCardId(query.id))
        return dto
