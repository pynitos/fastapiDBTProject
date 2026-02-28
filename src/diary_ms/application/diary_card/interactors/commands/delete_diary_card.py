from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.diary_card.dto.commands.delete_diary_card import DeleteDiaryCardCommand
from diary_ms.application.diary_card.interfaces.gateway import DiaryCardDeleter
from diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from diary_ms.domain.model.entities.user_id import UserId


class DeleteDiaryCard(CommandHandler[DeleteDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: DiaryCardDeleter,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteDiaryCardCommand) -> None:
        user_id: UserId = self._id_provider.get_current_user_id()
        id: DiaryCardId = DiaryCardId(command.id)
        await self._db_gateway.delete(id, user_id)
        await self._transaction_manager.commit()
