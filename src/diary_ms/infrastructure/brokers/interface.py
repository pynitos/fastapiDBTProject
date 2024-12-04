from typing import Any, Protocol


class Broker(Protocol):
    async def publish(self, message: Any, **kwargs: Any) -> Any | None:
        raise NotImplementedError

    async def request(self, message: Any, **kwargs: Any) -> Any | None:
        raise NotImplementedError

    async def connect(
        self,
        **kwargs: Any,
    ) -> Any:
        """Connect to Kafka servers manually.

        Consumes the same with `Broker.__init__` arguments and overrides them.
        To startup subscribers too you should use `broker.start()` after/instead this method.
        """
        raise NotImplementedError

    async def start(self) -> None:
        """ "Connect broker and startup all subscribers."""
        raise NotImplementedError

    async def ping(self, timeout: float | None) -> bool:
        raise NotImplementedError
