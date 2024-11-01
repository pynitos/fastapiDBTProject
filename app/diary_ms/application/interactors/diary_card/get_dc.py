from dataclasses import asdict

from app.diary_ms.application.dto.diary_card import GetOwnDiaryCardsDTO
from app.diary_ms.application.interactors.base import BaseInteractor
from app.diary_ms.application.interfaces.gateway import ReaderProtocol
from app.diary_ms.domain.models.diary_card import DiaryCardDM


class GetOwnDiaryCards(BaseInteractor[GetOwnDiaryCardsDTO, list[DiaryCardDM]]):
    def __init__(
            self,
            db_gateway: ReaderProtocol,
    ):
        self.db_gateway = db_gateway

    def __call__(self, data: GetOwnDiaryCardsDTO) -> DiaryCardDM:
        diary_cards: list[DiaryCardDM] = self.db_gateway.get_all(offset=data.pagination.offset,
                                                                 limit=data.pagination.limit)
        return diary_cards
