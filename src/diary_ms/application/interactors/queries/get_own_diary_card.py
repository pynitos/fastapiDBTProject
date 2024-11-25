from uuid import UUID
from src.diary_ms.application.common.interfaces.gateway import ReaderProtocol
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.dto.diary_card import OwnDiaryCardDTO
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetOwnDiaryCard(Interactor[UUID, OwnDiaryCardDTO | None]):
    def __init__(self, db_gateway: ReaderProtocol, id_provider: IdProvider):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    def __call__(self, id: UUID) -> OwnDiaryCardDTO | None:
        diary_card: OwnDiaryCardDTO | None = self.db_gateway.get_by_id(id)
        return diary_card
