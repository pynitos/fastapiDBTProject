from uuid import UUID

from src.diary_ms.application.common.interfaces.dispatcher.base import Dispatcher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.interfaces.gateway import DiaryCardSaver
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.entities.user_id import UserId


class CreateDiaryCard(CommandHandler[CreateDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: DiaryCardSaver,
        id_provider: IdProvider,
        uow: TransactionManager,
        mediator: Dispatcher,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow
        self.mediator = mediator

    async def __call__(self, command: CreateDiaryCardCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id.value
        diary_card: DiaryCard = DiaryCard.create(command)
        await self.db_gateway.create(diary_card)
        await self.mediator.publish(diary_card.pull_events())
        await self.uow.commit()
