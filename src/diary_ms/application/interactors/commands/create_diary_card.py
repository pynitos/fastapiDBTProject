from src.diary_ms.application.dto.diary_card import NewDiaryCardDTO
from src.diary_ms.application.interfaces.base import BaseInteractor
from src.diary_ms.application.interfaces.gateway import SaverProtocol
from src.diary_ms.application.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.entities import DiaryCardDM
from src.diary_ms.domain.model.entities import Id


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
