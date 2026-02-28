from typing import Any

from faststream.kafka.broker import KafkaBroker

from diary_ms.application.common.interfaces.types.base import BaseSendableMessage
from diary_ms.infrastructure.brokers.interface import (
    Broker,
    BrokerKeyType,
    BrokerTopicType,
)


class KafkaBrokerImpl(Broker):
    def __init__(self, broker_session: KafkaBroker):
        self.session = broker_session

    async def publish(
        self,
        message: BaseSendableMessage,
        topic: BrokerTopicType,
        key: BrokerKeyType = None,
    ) -> Any | None:
        return await self.session.publish(message, topic, key=key)

    async def start(self) -> None:
        """Connect broker and startup all subscribers."""
        await self.session.start()

    async def close(self) -> None:
        await self.session.close()

    async def ping(self, timeout: float | None) -> bool:
        return await self.session.ping(timeout=timeout)
