from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionAdminDeleter
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.emotion.delete_emotion import DeleteEmotionAdminCommand
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


class DeleteEmotionAdminHandler(CommandHandler[DeleteEmotionAdminCommand, None]):
    def __init__(
        self,
        db_gateway: EmotionAdminDeleter,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.transaction_manager = transaction_manager

    async def __call__(self, command: DeleteEmotionAdminCommand) -> None:
        self.id_provider.get_admin_user_id()
        await self.db_gateway.delete(EmotionId(command.id))
        await self.transaction_manager.commit()
