import logging

from src.diary_ms.application.common.interfaces.gateway import UpdaterProtocol
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.interactor import Interactor
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.domain.model.entities.user_id import UserId

logger = logging.getLogger()


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

    async def __call__(self, command: UpdateDiaryCardCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id
        old_diary_card: DiaryCardDM = await self.db_gateway.get_by_id(command.id)
        updated_diary_card: DiaryCardDM = old_diary_card.update(command=command)
        logger.info(str(updated_diary_card))
        await self.db_gateway.update(updated_diary_card)
        await self.uow.commit()
