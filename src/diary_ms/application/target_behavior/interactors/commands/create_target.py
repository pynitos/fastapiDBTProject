from src.diary_ms.application.common.interfaces.dispatcher.base import Publisher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.target_behavior.interfaces.gateway import TargetSaver
from src.diary_ms.domain.model.commands.target_behavior.create_target import CreateTargetCommand
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId


class CreateTarget(CommandHandler[CreateTargetCommand, None]):
    def __init__(
        self,
        db_gateway: TargetSaver,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self.db_gateway: TargetSaver = db_gateway
        self.id_provider: IdProvider = id_provider
        self._transaction_manager: TransactionManager = transaction_manager
        self._publisher: Publisher = publisher

    async def __call__(self, command: CreateTargetCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id.value
        medicament: Target = Target.create(command)
        await self.db_gateway.create(medicament)
        await self._transaction_manager.commit()
