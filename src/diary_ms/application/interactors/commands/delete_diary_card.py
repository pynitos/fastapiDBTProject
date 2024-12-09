from src.diary_ms.application.common.interfaces.diary_card import DeleterProtocol
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.commands.delete_diary_card import DeleteDiaryCardCommand


class DeleteDiaryCard(CommandHandler[DeleteDiaryCardCommand, None]):
    def __init__(
        self,
        db_gateway: DeleterProtocol,
        id_provider: IdProvider,
        uow: UOWProtocol,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, command: DeleteDiaryCardCommand) -> None:
        # user_id: UserId = self.id_provider.get_current_user_id()
        await self.db_gateway.delete(DiaryCardId(command.id))
        await self.uow.commit()
