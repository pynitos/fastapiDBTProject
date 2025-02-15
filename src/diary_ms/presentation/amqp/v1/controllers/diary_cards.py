from logging import getLogger
from uuid import UUID

from faststream.kafka import KafkaRouter

from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.presentation.amqp.deps import AMQPSenderDep

logger = getLogger(__name__)
AMQPDiaryCardController = KafkaRouter()


@AMQPDiaryCardController.subscriber("new_diary_card")
@AMQPDiaryCardController.publisher("diary_card_statuses")
async def handle(data: DiaryCardCreatedEvent, sender: AMQPSenderDep) -> UUID:  # noqa: ARG001
    # dto = NewBookDTO(
    #     title=data.title,
    #     pages=data.pages,
    #     is_read=data.is_read
    # )
    # uuid = await sender.send(dto)
    logger.info(f'diary card with id {data.diary_card_id} created.')
    return data.diary_card_id
