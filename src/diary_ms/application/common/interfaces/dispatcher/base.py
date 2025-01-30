from collections.abc import Iterable, Sequence
from typing import Any, Protocol

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.query import QRes, Query
from src.diary_ms.application.common.interfaces.handlers.command import (
    CR,
    CT,
    CommandHandler,
)
from src.diary_ms.application.common.interfaces.handlers.event import (
    ER,
    ET,
    EventHandler,
    EventListener,
)
from src.diary_ms.application.common.interfaces.handlers.query import (
    QR,
    QT,
    QueryHandler,
)
from src.diary_ms.domain.common.model.commands.commands import Command, CRes
from src.diary_ms.domain.common.model.events.base import Event


class Registry(Protocol):
    command_handlers: dict[type[Command[Any]], type[CommandHandler[Command[Any], Any]]]
    query_handlers: dict[type[Query[Any]], type[QueryHandler[Query[Any], Any]]]
    event_listeners: list[EventListener]

    def register_command_handler(self, command: type[CT], handler: type[CommandHandler[CT, CR]]) -> None:
        raise NotImplementedError

    def register_query_handler(self, query: type[QT], handler: type[QueryHandler[QT, QR]]) -> None:
        raise NotImplementedError

    def register_event_handler(self, event: type[ET], handler: type[EventHandler[ET, ER]]) -> None:
        raise NotImplementedError


class Sender(Protocol):
    async def send_command(self, command: Command[CRes]) -> CRes:
        raise NotImplementedError

    async def send_query(self, query: Query[QRes]) -> QRes:
        raise NotImplementedError


class Publisher(Protocol):
    async def publish(self, events: Event | Sequence[Event]) -> Iterable[DTO]:
        raise NotImplementedError


class Dispatcher(Sender, Publisher, Protocol): ...
