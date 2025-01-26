from src.diary_ms.application.admin.skill.interfaces.gateway import SkillAdminDeleter
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.domain.model.commands.skill.delete_skill import DeleteSkillAdminCommand
from src.diary_ms.domain.model.value_objects.skill.id import SkillId


class DeleteSkillAdminHandler(CommandHandler[DeleteSkillAdminCommand, None]):
    def __init__(
        self,
        db_gateway: SkillAdminDeleter,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.transaction_manager = transaction_manager

    async def __call__(self, command: DeleteSkillAdminCommand) -> None:
        self.id_provider.get_admin_user_id()
        await self.db_gateway.delete(SkillId(command.id))
        await self.transaction_manager.commit()
