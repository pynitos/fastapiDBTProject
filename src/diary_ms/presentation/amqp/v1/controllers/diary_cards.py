from logging import getLogger
from uuid import UUID

from dishka import FromDishka
from faststream.kafka import KafkaRouter

from src.diary_ms.application.common.interfaces.task_sender import TaskSender
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.presentation.amqp.deps import AMQPSenderDep

logger = getLogger(__name__)
AMQPDiaryCardController = KafkaRouter()


@AMQPDiaryCardController.subscriber("new_diary_card")
@AMQPDiaryCardController.publisher("diary_card_statuses")
async def handle(data: DiaryCardCreatedEvent, sender: AMQPSenderDep, task_sender: FromDishka[TaskSender]) -> UUID:  # noqa: ARG001
    task_sender.send_task('ok', 'diary_card_statuses', [{"cron": "*/1 */1 * * * *"}])
    logger.info(f"diary card with id {data.diary_card_id} created.")
    return data.diary_card_id
