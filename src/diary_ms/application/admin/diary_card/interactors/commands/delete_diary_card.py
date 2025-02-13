from src.diary_ms.application.admin.diary_card.interfaces.gateway import DiaryCardAdminDeleter
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.delete_diary_card import DeleteDiaryCardAdminCommand
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class DeleteDiaryCardAdminHandler(CommandHandler[DeleteDiaryCardAdminCommand, None]):
    def __init__(
        self,
        db_gateway: DiaryCardAdminDeleter,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteDiaryCardAdminCommand) -> None:
        self._id_provider.get_admin_user_id()
        await self._db_gateway.delete(DiaryCardId(command.id))
        await self._transaction_manager.commit()
