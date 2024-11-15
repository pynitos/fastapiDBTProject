from src.diary_ms.application.interfaces.gateway import SaverProtocol
from src.diary_ms.application.interfaces.id_provider import IdProvider
from src.diary_ms.application.interfaces.interactor import Interactor
from src.diary_ms.application.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.entities.user_id import UserId


class CreateDiaryCard(Interactor[CreateDiaryCardCommand, DiaryCardId]):
    def __init__(
            self,
            db_gateway: SaverProtocol,
            id_provider: IdProvider,
            uow: UOWProtocol,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, command: CreateDiaryCardCommand) -> DiaryCardId:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id
        diary_card: DiaryCardDM = DiaryCardDM.create(command)
        self.db_gateway.create(diary_card)
        await self.uow.commit()
        return diary_card.id
