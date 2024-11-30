from uuid import UUID

from src.diary_ms.application.common.interfaces.diary_card import DTOReader
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.dto.diary_card import OwnDiaryCardDTO


class GetOwnDiaryCard(Interactor[UUID, OwnDiaryCardDTO | None]):
    def __init__(self, db_gateway: DTOReader, id_provider: IdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    async def __call__(self, id: UUID) -> OwnDiaryCardDTO | None:
        diary_card: OwnDiaryCardDTO | None = await self.db_gateway.get_dto_by_id(id)
        return diary_card
