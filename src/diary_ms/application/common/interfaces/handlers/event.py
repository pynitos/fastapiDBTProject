from abc import abstractmethod
from typing import Generic, Protocol, TypeVar

from src.diary_ms.application.common.interfaces.handlers.base import Handler
from src.diary_ms.domain.common.model.events.base import BaseEvent

ET = TypeVar("ET", bound=BaseEvent, contravariant=True)
ER = TypeVar("ER", covariant=True)


class EventHandler(Handler[ET, ER], Protocol[ET, ER]):
    @abstractmethod
    async def __call__(self, event: ET) -> ER:
        raise NotImplementedError


EventHandlerType = EventHandler[ET, ER] | type[EventHandler[ET, ER]]


class EventListener(Generic[ET, ER]):
    def __init__(self, event: type[ET], handler: EventHandlerType[ET, ER]):
        self._event = event
        self._handler = handler

    def is_listen(self, event: BaseEvent) -> bool:
        return isinstance(event, self._event)

    @property
    def event(self) -> type[ET]:
        return self._event

    @property
    def handler(self) -> EventHandlerType[ET, ER]:
        return self._handler
