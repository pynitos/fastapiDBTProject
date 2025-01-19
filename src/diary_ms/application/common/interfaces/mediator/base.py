from collections.abc import Iterable, Sequence
from typing import Any, Protocol, TypeVar

from src.diary_ms.application.common.interfaces.handlers.command import (
    CommandHandler,
)
from src.diary_ms.application.common.interfaces.handlers.event import (
    ER,
    EventHandler,
)
from src.diary_ms.application.common.interfaces.handlers.query import (
    QueryHandler,
)
from src.diary_ms.domain.common.model.events.base import BaseEvent

CT = TypeVar("CT", bound=Any)
CR = Any
QT = TypeVar("QT", bound=Any)
QR = Any
ET = TypeVar("ET", bound=BaseEvent)


class Mediator(Protocol):
    def register_command_handler(
        self, command: type[CT], handler: CommandHandler[CT, CR]
    ) -> None:
        raise NotImplementedError

    def register_query_handler(
        self, query: type[QT], handler: QueryHandler[QT, QR]
    ) -> None:
        raise NotImplementedError

    def register_event_handler(
        self, event: type[ET], handler: EventHandler[ET, ER]
    ) -> None:
        raise NotImplementedError

    async def handle_command(self, command: Any) -> CR:
        raise NotImplementedError

    async def handle_query(self, query: Any) -> QR:
        raise NotImplementedError

    async def publish(self, events: BaseEvent | Sequence[BaseEvent]) -> Iterable[ER]:
        raise NotImplementedError
