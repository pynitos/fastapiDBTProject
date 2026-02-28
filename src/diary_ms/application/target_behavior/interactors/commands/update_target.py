import logging

from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.target_behavior.dto.commands.update_target import UpdateTargetCommand
from diary_ms.application.target_behavior.exceptions.target_behavior import TargetNotFoundError
from diary_ms.application.target_behavior.interfaces.gateway import TargetUpdater
from diary_ms.domain.model.entities.target_behavior import Target
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge

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
        medicament_id: TargetId = TargetId(command.target_id)
        old_target: Target | None = await self._db_gateway.get_by_id(medicament_id, user_id)
        if not old_target:
            raise TargetNotFoundError(medicament_id)
        new_target: Target = old_target.update(
            urge=TargetUrge(command.urge) if command.urge else None,
            action=CopingAction(command.action) if command.action else None,
        )
        await self._db_gateway.update(new_target)
        await self._transaction_manager.commit()
        logger.debug(f"Diary card with id: {command.target_id} updated.")
