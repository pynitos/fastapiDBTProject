import logging

from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.target_behavior.exceptions.target_behavior import TargetNotFoundError
from src.diary_ms.application.target_behavior.interfaces.gateway import TargetUpdater
from src.diary_ms.domain.model.commands.target_behavior.update_target import UpdateTargetCommand
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId

logger: logging.Logger = logging.getLogger()


class UpdateTarget(CommandHandler[UpdateTargetCommand, None]):
    def __init__(
        self,
        db_gateway: TargetUpdater,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateTargetCommand) -> None:
        user_id: UserId = self._id_provider.get_current_user_id()
        medicament_id: TargetId = TargetId(command.id)
        old_target: Target | None = await self._db_gateway.get_by_id(medicament_id, user_id)
        if not old_target:
            raise TargetNotFoundError(medicament_id)
        new_target: Target = old_target.update(command=command)
        await self._db_gateway.update(new_target)
        await self._transaction_manager.commit()
        logger.debug(f"Diary card with id: {command.id} updated.")
