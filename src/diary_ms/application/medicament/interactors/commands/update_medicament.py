import logging

from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.medicament.dto.commands.update_medicament import UpdateMedicamentCommand
from diary_ms.application.medicament.exceptions.medicament import MedicamentNotFoundError
from diary_ms.application.medicament.interfaces.gateway import MedicamentUpdater
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from diary_ms.domain.model.value_objects.medicament.name import MedicamentName

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
        new_med: Medicament = old_med.update(
            name=MedicamentName(command.name) if command.name else None,
            dosage=MedicamentDosage(command.dosage) if command.dosage else None,
        )
        await self._db_gateway.update(new_med)
        await self._transaction_manager.commit()
        logger.debug(f"Diary card with id: {command.id} updated.")
