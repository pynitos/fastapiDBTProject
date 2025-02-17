import logging

from src.diary_ms.application.common.interfaces.handlers.event import EventHandler
from src.diary_ms.application.common.interfaces.task_sender import TaskSender
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.infrastructure.brokers.interface import Broker

logger = logging.getLogger(__name__)


class DiaryCardCreatedEventHandler(EventHandler[DiaryCardCreatedEvent, None]):
    def __init__(
        self,
        message_broker: Broker,
        task_sender: TaskSender,
    ) -> None:
        self._task_sender = task_sender
        self._message_broker = message_broker

    async def __call__(self, event: DiaryCardCreatedEvent) -> None:
        await self._message_broker.publish(message=event, topic="new_diary_card")
        await self._task_sender.send_task("task message", topic="get_diary_cards", schedule=[{"cron": "*/1 * * * * *"}])
        # result = await self._task_sender.get_result(task_id)
        # logger.info(result)
