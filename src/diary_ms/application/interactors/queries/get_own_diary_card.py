from src.diary_ms.application.interfaces.gateway import ReaderProtocol
from src.diary_ms.application.interfaces.id_provider import IdProvider
from src.diary_ms.application.interfaces.interactor import Interactor
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetOwnDiaryCards(Interactor[DiaryCardId, DiaryCardDM]):
    def __init__(
            self,
            db_gateway: ReaderProtocol,
            id_provider: IdProvider
    ):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    def __call__(self, id: DiaryCardId) -> DiaryCardDM:
        diary_card: DiaryCardDM = self.db_gateway.get_by_id(id)
        return diary_card
