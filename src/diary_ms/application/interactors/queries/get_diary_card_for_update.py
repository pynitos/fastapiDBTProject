from uuid import UUID

from src.diary_ms.application.common.interfaces.gateway import (
    DTOForUpdateReader,
)
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.dto.for_update_diary_card import DiaryCardForUpdateDTO
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM


class GetDiaryCardForUpdate(Interactor[UUID, DiaryCardForUpdateDTO | None]):
    def __init__(self, db_gateway: DTOForUpdateReader, id_provider: IdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, id: UUID) -> DiaryCardForUpdateDTO | None:
        diary_card: DiaryCardDM | None = await self.db_gateway.get_by_id(id)
        if diary_card:
            diary_card: GetDiaryCardForUpdate = (
                await self.db_gateway.get_dto_for_update(diary_card)
            )
        return diary_card
