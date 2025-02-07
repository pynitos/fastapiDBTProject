from src.diary_ms.application.common.interfaces.dispatcher.base import Publisher
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentSaver
from src.diary_ms.domain.model.commands.medicament.create_medicament import CreateMedicamentAdminCommand, CreateMedicamentCommand
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.user_id import UserId


class CreateMedicament(CommandHandler[CreateMedicamentAdminCommand, None]):
    def __init__(
        self,
        db_gateway: MedicamentSaver,
        id_provider: IdProvider,
        transaction_manager: TransactionManager,
        publisher: Publisher,
    ) -> None:
        self.db_gateway: MedicamentSaver = db_gateway
        self.id_provider: IdProvider = id_provider
        self._transaction_manager: TransactionManager = transaction_manager
        self._publisher: Publisher = publisher

    async def __call__(self, command: CreateMedicamentAdminCommand) -> None:
        user_id: UserId = self.id_provider.get_current_user_id()
        command.user_id = user_id.value
        medicament: Medicament = Medicament.admin_create(command)
        await self.db_gateway.create(medicament)
        await self._transaction_manager.commit()
