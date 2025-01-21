from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from dishka import AsyncContainer

from src.diary_ms.application.common.exceptions.base import HandlerNotFoundError
from src.diary_ms.application.common.interfaces.dispatcher.base import Dispatcher
from src.diary_ms.application.common.interfaces.dispatcher.resolver import Resolver
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
from src.diary_ms.domain.common.model.events.base import BaseEvent

CT = TypeVar("CT", bound=Any)
CR = Any
QT = TypeVar("QT", bound=Any)
QR = Any
ET = TypeVar("ET", bound=BaseEvent)


class DishkaResolver[T](Resolver):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve(self, dependency_type: type[T]) -> T:
        return await self._container.get(dependency_type)


class Registry:
    def __init__(self) -> None:
        self._command_handlers: dict[type[Any], CommandHandlerType[Any, Any]] = {}
        self._query_handlers: dict[type[Any], QueryHandlerType[Any, Any]] = {}
        self._event_listeners: list[EventListener[Any, Any]] = []

    def register_command_handler(self, command: type[CT], handler: CommandHandlerType[Any, Any]) -> None:
        self._command_handlers[command] = handler

    def register_query_handler(self, query: type[QT], handler: QueryHandlerType[Any, Any]) -> None:
        self._query_handlers[query] = handler

    def register_event_handler(self, event: type[ET], handler: EventHandlerType[ET, Any]) -> None:
        listener = EventListener[Any, Any](event, handler)
        self._event_listeners.append(listener)


class DispatcherImpl(Dispatcher):
    def __init__(self, resolver: Resolver, registry: Registry) -> None:
        self._resolver = resolver
        self._registry = registry

    async def handle_command(self, command: Any) -> CR:
        handler: CommandHandlerType[Any, Any] | None = self._registry._command_handlers.get(type(command))
        if not handler:
            raise HandlerNotFoundError()
        handler = self._resolver.resolve(handler)
        return await handler(command)

    async def handle_query(self, query: Any) -> QR:
        handler: QueryHandlerType[Any, Any] | None = self._registry._query_handlers.get(type(query))
        if not handler:
            raise HandlerNotFoundError()
        handler = self._resolver.resolve(handler)
        return await handler(query)

    async def publish(self, events: BaseEvent | Sequence[BaseEvent]) -> Iterable[ER]:
        if not isinstance(events, Sequence):
            events = [events]
        result = []
        for event in events:
            for listener in self._registry._event_listeners:
                if listener.is_listen(event):
                    handler = self._resolver.resolve(listener.handler(event))
                    result.extend([await handler])
        return result
