from src.diary_ms.application.admin.target_behavior.interfaces.gateway import TargetAdminDeleter
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.domain.model.commands.target_behavior.delete_target import (
    DeleteTargetAdminCommand,
)
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class DeleteTargetAdminHandler(CommandHandler[DeleteTargetAdminCommand, None]):
    def __init__(
        self,
        db_gateway: TargetAdminDeleter,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteTargetAdminCommand) -> None:
        self._id_provider.get_admin_user_id()
        medicament_id: TargetId = TargetId(command.id)
        await self._db_gateway.delete(medicament_id)
        await self._transaction_manager.commit()
