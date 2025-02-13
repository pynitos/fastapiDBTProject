import logging

from src.diary_ms.application.admin.emotion.interfaces.gateway import EmotionAdminUpdater
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.emotion.update_emotion import UpdateEmotionAdminCommand
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.value_objects.emotion.description import EmotionDescription
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName

logger = logging.getLogger()


class UpdateEmotionAdminHandler(CommandHandler[UpdateEmotionAdminCommand, None]):
    def __init__(
        self,
        db_gateway: EmotionAdminUpdater,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self.transaction_manager = transaction_manager

    async def __call__(self, command: UpdateEmotionAdminCommand) -> None:
        self._id_provider.get_admin_user_id()
        emotion: Emotion | None = await self._db_gateway.get_by_id(EmotionId(command.id))
        if emotion:
            updated_emotion: Emotion = emotion.update(
                name=EmotionName(command.name) if command.name else None,
                description=EmotionDescription(command.description) if command.description else None,
            )
            await self._db_gateway.update(updated_emotion)
            logger.debug(f"Emotion with id: {command.id} updated.")
            await self.transaction_manager.commit()
