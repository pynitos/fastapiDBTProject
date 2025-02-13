from uuid import uuid4

from src.diary_ms.application.admin.target_behavior.interfaces.gateway import TargetAdminSaver
from src.diary_ms.application.common.interfaces.dispatcher.base import Publisher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.target_behavior.dto.commands.create_target import CreateTargetAdminCommand
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.target_behavior.action import TargetAction
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge


class CreateTargetAdminHandler(CommandHandler[CreateTargetAdminCommand, None]):
    def __init__(
        self,
        db_gateway: TargetAdminSaver,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager
        self._publisher = publisher

    async def __call__(self, command: CreateTargetAdminCommand) -> None:
        user_id: UserId = self._id_provider.get_admin_user_id()
        command.user_id = user_id.value
        command.is_default = True
        medicament: Target = Target.admin_create(
            id=TargetId(uuid4()),
            user_id=user_id,
            urge=TargetUrge(command.urge),
            action=TargetAction(command.action),
            is_default=TargetIsDefault(command.is_default),
        )
        await self._db_gateway.create(medicament)
        await self._transaction_manager.commit()
