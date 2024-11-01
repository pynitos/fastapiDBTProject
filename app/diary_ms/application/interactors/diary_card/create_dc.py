from app.diary_ms.application.dto.diary_card import NewDiaryCardDTO
from app.diary_ms.application.interactors.base import BaseInteractor
from app.diary_ms.application.interfaces.gateway import SaverProtocol
from app.diary_ms.application.interfaces.uow import UOWProtocol
from app.diary_ms.domain.models.diary_card import DiaryCardDM
from app.diary_ms.domain.models.id import Id


class CreateDiaryCard(BaseInteractor[NewDiaryCardDTO, Id]):
    def __init__(
            self,
            db_gateway: SaverProtocol,
            uow: UOWProtocol,
    ):
        self.db_gateway = db_gateway
        self.uow = uow

    def __call__(self, data: NewDiaryCardDTO) -> Id:
        diary_card = data
        diary_card: DiaryCardDM = self.db_gateway.create(diary_card)
        self.uow.commit()
        return diary_card.id
