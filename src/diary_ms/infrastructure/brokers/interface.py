from datetime import datetime
from typing import Any, Protocol

type BrokerMessageType = str | bytes | datetime | bool | None
type BrokerKeyType = bytes | Any | None
type BrokerTopicType = str


class Broker(Protocol):
    async def publish(self, message: BrokerMessageType, topic: Any) -> Any | None:
        raise NotImplementedError

    async def start(self) -> None:
        """ "Connect broker and startup all subscribers."""
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def ping(self, timeout: float | None) -> bool:
        raise NotImplementedError
