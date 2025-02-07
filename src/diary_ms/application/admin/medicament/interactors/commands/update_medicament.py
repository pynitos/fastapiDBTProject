import logging

from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.medicament.exceptions.medicament import MedicamentNotFoundError
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentUpdater
from src.diary_ms.domain.model.commands.medicament.update_medicament import UpdateMedicamentCommand
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId

logger = logging.getLogger()


class UpdateMedicament(CommandHandler[UpdateMedicamentCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentUpdater,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateMedicamentCommand) -> None:
        user_id: UserId = self._id_provider.get_current_user_id()
        medicament_id: MedicamentId = MedicamentId(command.id)
        old_med: Medicament | None = await self._db_gateway.get_by_id(medicament_id, user_id)
        if not old_med:
            raise MedicamentNotFoundError(medicament_id)
        new_med: Medicament = old_med.update(command=command)
        await self._db_gateway.update(new_med)
        await self._transaction_manager.commit()
        logger.debug(f"Diary card with id: {command.id} updated.")
