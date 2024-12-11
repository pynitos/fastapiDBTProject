from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from src.diary_ms.application.common.exceptions.base import HandlerNotFoundError
from src.diary_ms.application.common.interfaces.handlers.command import (
    CommandHandlerType,
)
from src.diary_ms.application.common.interfaces.handlers.event import (
    ER,
    EventHandlerType,
    EventListener,
)
from src.diary_ms.application.common.interfaces.handlers.query import (
    QueryHandlerType,
)
from src.diary_ms.application.common.interfaces.mediator.base import Mediator
from src.diary_ms.domain.common.model.events.base import BaseEvent

CT = TypeVar("CT", bound=Any)
CR = Any | None
QT = TypeVar("QT", bound=Any)
QR = Any | None
ET = TypeVar("ET", bound=BaseEvent)


class MediatorImpl(Mediator):
    def __init__(self) -> None:
        self._command_handlers: dict[type[Any], CommandHandlerType[Any, Any]] = {}
        self._query_handlers: dict[type[Any], QueryHandlerType[Any, Any]] = {}
        self._event_listeners: list[EventListener[BaseEvent, Any]] = []

    def register_command_handler(
        self, command: type[CT], handler: CommandHandlerType[Any, Any]
    ) -> None:
        self._command_handlers[command] = handler

    def register_query_handler(
        self, query: type[QT], handler: QueryHandlerType[Any, Any]
    ) -> None:
        self._query_handlers[query] = handler

    def register_event_handler(
        self, event: type[ET], handler: EventHandlerType[BaseEvent, Any]
    ) -> None:
        listener = EventListener[BaseEvent, Any](event, handler)
        self._event_listeners.append(listener)

    async def handle_command(self, command: Any) -> CR:
        handler: CommandHandlerType[Any, Any] | None = self._command_handlers.get(
            type(command)
        )
        if not handler:
            raise HandlerNotFoundError()
        return await handler(command)

    async def handle_query(self, query: Any) -> QR:
        handler: QueryHandlerType[Any, Any] | None = self._query_handlers.get(
            type(query)
        )
        if not handler:
            raise HandlerNotFoundError()
        return await handler(query)

    async def publish(self, events: BaseEvent | Sequence[BaseEvent]) -> Iterable[ER]:
        if not isinstance(events, Sequence):
            events = [events]
        result = []
        for event in events:
            for listener in self._event_listeners:
                if listener.is_listen(event):
                    result.extend([await listener.handler(event)])
        return result
