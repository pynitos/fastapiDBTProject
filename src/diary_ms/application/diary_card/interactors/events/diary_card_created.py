from src.diary_ms.application.common.interfaces.handlers.event import EventHandler
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.infrastructure.brokers.interface import Broker


class DiaryCardCreatedEventHandler(EventHandler[DiaryCardCreatedEvent, None]):
    def __init__(self, broker: Broker) -> None:
        self.broker = broker

    async def __call__(self, event: DiaryCardCreatedEvent) -> None:
        await self.broker.publish(message=event, topic="new_diary_card")
