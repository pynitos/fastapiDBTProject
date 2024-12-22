
from uuid import UUID
from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionSaver
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.mediator.base import Mediator
from src.diary_ms.application.common.interfaces.uow import UOWProtocol
from src.diary_ms.domain.model.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.domain.model.commands.create_emotion import CreateEmotionCommand
from src.diary_ms.domain.model.entities.emotion import EmotionDM


class AdminCreateEmotion(CommandHandler[CreateEmotionCommand, None]):
    def __init__(
        self,
        db_gateway: EmotionSaver,
        id_provider: AdminIdProvider,
        uow: UOWProtocol,
        mediator: Mediator,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.uow = uow
        self.mediator = mediator

    async def __call__(self, command: CreateEmotionCommand) -> None:
        user_id: UUID = self.id_provider.get_current_user_id()
        command.user_id = user_id
        emotion: EmotionDM = EmotionDM.create(command)
        await self.db_gateway.create(emotion)
        await self.mediator.publish(emotion.pull_events())
        await self.uow.commit()
