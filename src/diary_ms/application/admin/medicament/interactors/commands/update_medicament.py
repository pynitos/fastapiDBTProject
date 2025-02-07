import logging

from src.diary_ms.application.admin.medicament.interfaces.gateway import MedicamentAdminUpdater
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.medicament.exceptions.medicament import MedicamentNotFoundError
from src.diary_ms.domain.model.commands.medicament.update_medicament import (
    UpdateMedicamentAdminCommand,
)
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId

logger = logging.getLogger()


class UpdateMedicamentAdminHandler(CommandHandler[UpdateMedicamentAdminCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentAdminUpdater,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateMedicamentAdminCommand) -> None:
        self._id_provider.get_admin_user_id()
        medicament_id: MedicamentId = MedicamentId(command.id)
        old_med: Medicament | None = await self._db_gateway.get_by_id(medicament_id, user_id)
        if not old_med:
            raise MedicamentNotFoundError(medicament_id)
        new_med: Medicament = old_med.update(command=command)
        await self._db_gateway.update(new_med)
        await self._transaction_manager.commit()
        logger.debug(f"Medicament with id: {command.id} updated.")
