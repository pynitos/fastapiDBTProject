from src.diary_ms.application.admin.diary_card.dto.diary_card import DiaryCardAdminDTO, GetDiaryCardAdminDTO
from src.diary_ms.application.admin.diary_card.dto.mappers.diary_card import DiaryCardAdminDTOMapper
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardReader
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetDiaryCard(QueryHandler[GetDiaryCardAdminDTO, DiaryCardAdminDTO]):
    def __init__(self, db_gateway: DiaryCardReader, id_provider: IdProvider):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = DiaryCardAdminDTOMapper

    async def __call__(self, query: GetDiaryCardAdminDTO) -> DiaryCardAdminDTO:
        diary_card: DiaryCard | None = await self._db_gateway.get_by_id(DiaryCardId(query.id))
        if not diary_card:
            raise DiaryCardNotFoundError
        return self._mapper.dm_to_dto(diary_card)
