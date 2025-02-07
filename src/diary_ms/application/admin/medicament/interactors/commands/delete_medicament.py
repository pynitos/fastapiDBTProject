from src.diary_ms.application.admin.medicament.interfaces.gateway import MedicamentAdminDeleter
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.domain.model.commands.medicament.delete_medicament import (
    DeleteMedicamentAdminCommand,
)
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class DeleteMedicamentAdminHandler(CommandHandler[DeleteMedicamentAdminCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentAdminDeleter,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteMedicamentAdminCommand) -> None:
        self._id_provider.get_admin_user_id()
        medicament_id: MedicamentId = MedicamentId(command.id)
        await self._db_gateway.delete(medicament_id)
        await self._transaction_manager.commit()
