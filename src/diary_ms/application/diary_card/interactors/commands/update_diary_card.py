import logging

from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardUpdater
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.update_diary_card import UpdateDiaryCardCommand

logger = logging.getLogger()


class UpdateDiaryCard(CommandHandler[UpdateDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: DiaryCardUpdater,
        id_provider: IdProvider,
        uow: UOWProtocol,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, command: UpdateDiaryCardCommand) -> None:
        # user_id: UserId = self.id_provider.get_current_user_id()
        old_diary_card: DiaryCard | None = await self.db_gateway.get_by_id(DiaryCardId(command.id))
        if old_diary_card:
            updated_diary_card: DiaryCard = old_diary_card.update(command=command)
            await self.db_gateway.update(updated_diary_card)
            logger.debug(f"Diary card with id: {command.id} updated.")
            await self.uow.commit()
        return None
