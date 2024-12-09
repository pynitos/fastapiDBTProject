from src.diary_ms.application.common.interfaces.handlers.event import EventHandler
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.infrastructure.brokers.converters.base import (
    convert_event_to_broker_message,
)
from src.diary_ms.infrastructure.brokers.interface import Broker


class DiaryCardCreatedEventHandler(EventHandler[DiaryCardCreatedEvent, None]):
    def __init__(self, broker: Broker) -> None:
        self.broker = broker

    async def __call__(self, event: DiaryCardCreatedEvent) -> None:
        message: bytes = convert_event_to_broker_message(event)
        await self.broker.publish(message=message, topic="new_diary_card_topic")
