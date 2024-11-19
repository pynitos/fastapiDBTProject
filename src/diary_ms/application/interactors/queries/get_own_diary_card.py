from src.diary_ms.application.common.interfaces.gateway import ReaderProtocol
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class GetOwnDiaryCard(Interactor[DiaryCardId, DiaryCardDM | None]):
    def __init__(
            self,
            db_gateway: ReaderProtocol,
            id_provider: IdProvider
    ):
        self.db_gateway = db_gateway
        self.id_provider = id_provider

    def __call__(self, id: DiaryCardId) -> DiaryCardDM | None:
        diary_card: DiaryCardDM | None = self.db_gateway.get_by_id(id)
        return diary_card
