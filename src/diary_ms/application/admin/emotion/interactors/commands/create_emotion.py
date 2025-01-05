from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionAdminSaver
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionAdminCommand
from src.diary_ms.domain.model.entities.emotion import EmotionDM


class CreateEmotionAdminHandler(CommandHandler[CreateEmotionAdminCommand, None]):
    def __init__(
        self,
        db_gateway: EmotionAdminSaver,
        id_provider: AdminIdProvider,
        uow: UOWProtocol,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, command: CreateEmotionAdminCommand) -> None:
        self.id_provider.get_admin_user_id()
        emotion: EmotionDM = EmotionDM.create(command)
        await self.db_gateway.create(emotion)
        await self.uow.commit()
