from uuid import UUID

from src.diary_ms.application.common.interfaces.dispatcher.base import Publisher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentSaver
from src.diary_ms.domain.model.commands.medicament.create_medicament import CreateMedicamentCommand
from src.diary_ms.domain.model.entities.medicament import Medicament


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
        user_id: UUID = self.id_provider.get_current_user_id()
        command.user_id = user_id
        medicament: Medicament = Medicament.create(command)
        await self.db_gateway.create(medicament)
        await self._transaction_manager.commit()
