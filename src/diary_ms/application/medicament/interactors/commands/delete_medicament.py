from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.medicament.dto.commands.delete_medicament import DeleteMedicamentCommand
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentDeleter
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class DeleteMedicament(CommandHandler[DeleteMedicamentCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentDeleter,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteMedicamentCommand) -> None:
        user_id: UserId = self._id_provider.get_current_user_id()
        medicament_id: MedicamentId = MedicamentId(command.id)
        await self._db_gateway.delete(medicament_id, user_id)
        await self._transaction_manager.commit()
