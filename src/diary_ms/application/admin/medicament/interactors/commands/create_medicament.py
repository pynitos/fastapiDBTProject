from src.diary_ms.application.common.interfaces.dispatcher.base import Publisher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentSaver
from src.diary_ms.domain.model.commands.medicament.create_medicament import (
    CreateMedicamentAdminCommand,
)
from src.diary_ms.domain.model.entities.medicament import Medicament


class CreateMedicamentAdminHandler(CommandHandler[CreateMedicamentAdminCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentSaver,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self.db_gateway: MedicamentSaver = db_gateway
        self.id_provider: AdminIdProvider = id_provider
        self._transaction_manager: TransactionManager = transaction_manager
        self._publisher: Publisher = publisher

    async def __call__(self, command: CreateMedicamentAdminCommand) -> None:
        self.id_provider.get_admin_user_id()
        medicament: Medicament = Medicament.admin_create(command)
        await self.db_gateway.create(medicament)
        await self._transaction_manager.commit()
