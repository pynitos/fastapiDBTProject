from uuid import uuid4

from diary_ms.application.common.interfaces.dispatcher.base import Publisher
from diary_ms.application.common.interfaces.handlers.command import CommandHandler
from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.medicament.dto.commands.create_medicament import CreateMedicamentCommand
from diary_ms.application.medicament.interfaces.gateway import MedicamentSaver
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from diary_ms.domain.model.value_objects.medicament.name import MedicamentName


class CreateMedicament(CommandHandler[CreateMedicamentCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentSaver,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CreateMedicamentCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id.value
        medicament: Medicament = Medicament.create(
            id=MedicamentId(uuid4()),
            user_id=user_id,
            name=MedicamentName(command.name),
            dosage=MedicamentDosage(command.dosage),
        )
        await self.db_gateway.create(medicament)
        await self._transaction_manager.commit()
