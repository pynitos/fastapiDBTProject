from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from dishka import AsyncContainer

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.application.common.exceptions.base import HandlerNotFoundError
from src.diary_ms.application.common.interfaces.dispatcher.base import Dispatcher, Registry
from src.diary_ms.application.common.interfaces.dispatcher.resolver import Resolver
from src.diary_ms.application.common.interfaces.handlers.command import (
    CommandHandler,
)
from src.diary_ms.application.common.interfaces.handlers.event import (
    EventHandler,
    EventListener,
)
from src.diary_ms.application.common.interfaces.handlers.query import (
    QueryHandler,
)
from src.diary_ms.domain.common.model.commands.commands import Command
from src.diary_ms.domain.common.model.events.base import Event

TDependency = TypeVar("TDependency")


class DishkaResolver(Resolver):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve(self, dependency_type: type[TDependency]) -> TDependency:
        return await self._container.get(dependency_type)


class RegistryImpl(Registry):
    command_handlers: dict[type[Command[Any]], type[CommandHandler[Any, Any]]]
    query_handlers: dict[type[Query[DTO]], type[QueryHandler[Query[DTO], DTO]]]
    event_listeners: list[EventListener]

    def __init__(self) -> None:
        self.command_handlers = {}
        self.query_handlers = {}
        self.event_listeners = []

    def register_command_handler(self, command: type[Command[Any]], handler: type[CommandHandler[Any, Any]]) -> None:
        self.command_handlers[command] = handler

    def register_query_handler(self, query: type[Query[Any]], handler: type[QueryHandler[Any, Any]]) -> None:
        self.query_handlers[query] = handler

    def register_event_handler(self, event: type[Event], handler: type[EventHandler[Any, Any]]) -> None:
        listener = EventListener(event, handler)
        self.event_listeners.append(listener)


class DispatcherImpl(Dispatcher):
    def __init__(self, resolver: Resolver, registry: Registry) -> None:
        self._resolver = resolver
        self._registry = registry

    async def send_command(self, command: Command[Any]) -> Any:
        handler_: type[CommandHandler[Command[Any], Any]] | None = self._registry.command_handlers.get(type(command))
        if not handler_:
            raise HandlerNotFoundError()
        handler: CommandHandler[Command[Any], Any] = await self._resolver.resolve(handler_)
        return await handler(command)

    async def send_query(self, query: Query[Any]) -> Any:
        handler_: type[QueryHandler[Any, Any]] | None = self._registry.query_handlers.get(type(query))
        if not handler_:
            raise HandlerNotFoundError()
        handler: QueryHandler[Query[Any], Any] = await self._resolver.resolve(handler_)
        return await handler(query)

    async def publish(self, events: Event | Sequence[Event]) -> Iterable[DTO]:
        if not isinstance(events, Sequence):
            events = [events]
        result: list[Any] = []
        for event in events:
            for listener in self._registry.event_listeners:
                if listener.is_listen(event):
                    handler = await self._resolver.resolve(listener.handler)
                    result.extend([await handler(event)])
        return result
