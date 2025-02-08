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
from src.diary_ms.domain.model.entities.user_id import UserId


class GetDiaryCardForUpdate(QueryHandler[GetDiaryCardForUpdateDTO, DiaryCardForUpdateDTO]):
    def __init__(self, db_gateway: DiaryCardDTOForUpdateReader, id_provider: IdProvider):
        self._db_gateway = db_gateway
        self._id_provider = id_provider

    async def __call__(self, query: GetDiaryCardForUpdateDTO) -> DiaryCardForUpdateDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        dto: DiaryCardForUpdateDTO = await self._db_gateway.get_dto_for_update(DiaryCardId(query.id), user_id)
        return dto
