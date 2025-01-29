from abc import abstractmethod
from typing import Protocol, TypeVar

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.interfaces.handlers.base import Handler
from src.diary_ms.domain.common.model.events.base import Event

ET = TypeVar("ET", bound=Event, contravariant=True)
ER = TypeVar("ER", bound=DTO | None, covariant=True)


class EventHandler(Handler[ET, ER], Protocol[ET, ER]):
    @abstractmethod
    async def __call__(self, event: ET) -> ER:
        raise NotImplementedError


class EventListener:
    def __init__(self, event: type[Event], handler: type[EventHandler[Event, DTO | None]]):
        self._event = event
        self._handler = handler

    def is_listen(self, event: Event) -> bool:
        return isinstance(event, self._event)

    @property
    def event(self) -> type[Event]:
        return self._event

    @property
    def handler(self) -> type[EventHandler[Event, DTO | None]]:
        return self._handler
