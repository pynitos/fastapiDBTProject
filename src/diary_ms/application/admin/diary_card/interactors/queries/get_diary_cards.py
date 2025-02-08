from src.diary_ms.application.admin.diary_card.dto.diary_card import DiaryCardAdminDTO, GetDiaryCardsAdminDTO
from src.diary_ms.application.admin.diary_card.dto.mappers.diary_card import DiaryCardAdminDTOMapper
from src.diary_ms.application.admin.diary_card.interfaces.gateway import DiaryCardAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard


class GetDiaryCardsAdminHandler(QueryHandler[GetDiaryCardsAdminDTO, list[DiaryCardAdminDTO]]):
    def __init__(
        self,
        db_gateway: DiaryCardAdminReader,
        id_provider: AdminIdProvider,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = DiaryCardAdminDTOMapper

    async def __call__(self, query: GetDiaryCardsAdminDTO) -> list[DiaryCardAdminDTO]:
        diary_cards: list[DiaryCard] = await self._db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )
        return self._mapper.dm_list_to_dto_list(diary_cards)
