from typing import Any, Protocol

from src.diary_ms.application.common.interfaces.types.base import BaseSendableMessage

type BrokerKeyType = bytes | Any | None
type BrokerTopicType = str


class Broker(Protocol):
    async def publish(self, message: BaseSendableMessage, topic: Any) -> Any | None:
        raise NotImplementedError

    async def start(self) -> None:
        """Connect broker and startup all subscribers."""
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def ping(self, timeout: float | None) -> bool:
        raise NotImplementedError
