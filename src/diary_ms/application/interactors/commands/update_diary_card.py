from src.diary_ms.application.common.interfaces.gateway import SaverProtocol, UpdaterProtocol
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.entities.user_id import UserId


class UpdateDiaryCard(Interactor[UpdateDiaryCardCommand, None]):
    def __init__(
            self,
            db_gateway: UpdaterProtocol,
            id_provider: IdProvider,
            uow: UOWProtocol,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow

    def __call__(self, command: UpdateDiaryCardCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id
        diary_card: DiaryCardDM = DiaryCardDM.update(command=command)
        self.db_gateway.update(diary_card)
        self.uow.commit()
