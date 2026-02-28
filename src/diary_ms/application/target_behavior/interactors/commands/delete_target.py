from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.target_behavior.dto.commands.delete_target import DeleteTargetCommand
from diary_ms.application.target_behavior.interfaces.gateway import TargetDeleter
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class DeleteTarget(CommandHandler[DeleteTargetCommand, None]):
    def __init__(
        self,
        db_gateway: TargetDeleter,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteTargetCommand) -> None:
        user_id: UserId = self._id_provider.get_current_user_id()
        medicament_id: TargetId = TargetId(command.id)
        await self._db_gateway.delete(medicament_id, user_id)
        await self._transaction_manager.commit()
