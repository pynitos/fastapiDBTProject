from uuid import uuid4

from diary_ms.application.common.interfaces.dispatcher.base import Publisher
from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.target_behavior.dto.commands.create_target import CreateTargetCommand
from diary_ms.application.target_behavior.interfaces.gateway import TargetSaver
from diary_ms.domain.model.entities.target_behavior import Target
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge


class CreateTarget(CommandHandler[CreateTargetCommand, None]):
    def __init__(
        self,
        db_gateway: TargetSaver,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self._db_gateway: TargetSaver = db_gateway
        self._id_provider: IdProvider = id_provider
        self._transaction_manager: TransactionManager = transaction_manager
        self._publisher: Publisher = publisher

    async def __call__(self, command: CreateTargetCommand) -> None:
        user_id: UserId = self._id_provider.get_current_user_id()
        command.user_id = user_id.value
        target: Target = Target.create(
            id=TargetId(uuid4()),
            user_id=user_id,
            urge=TargetUrge(command.urge),
            action=CopingAction(command.action) if command.action else None,
        )
        await self._db_gateway.create(target)
        await self._transaction_manager.commit()
