from abc import abstractmethod
from typing import Protocol, TypeVar

from diary_ms.application.common.dto.base import ResultDTO
from diary_ms.application.common.interfaces.handlers.base import Handler
from diary_ms.domain.common.model.events.base import Event

ET = TypeVar("ET", bound=Event, contravariant=True)
ER = TypeVar("ER", bound=ResultDTO | None, covariant=True)


class EventHandler(Handler[ET, ER], Protocol[ET, ER]):
    @abstractmethod
    async def __call__(self, event: ET) -> ER:
        raise NotImplementedError


class EventListener:
    def __init__(self, event: type[Event], handler: type[EventHandler[Event, ResultDTO | None]]):
        self._event = event
        self._handler = handler

    def is_listen(self, event: Event) -> bool:
        return isinstance(event, self._event)

    @property
    def event(self) -> type[Event]:
        return self._event

    @property
    def handler(self) -> type[EventHandler[Event, ResultDTO | None]]:
        return self._handler
