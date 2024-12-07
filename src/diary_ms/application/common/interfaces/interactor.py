from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol, TypeVar

from src.diary_ms.domain.common.model.events.base import BaseEvent
from src.diary_ms.infrastructure.brokers.interface import Broker


class Interactor[InputDTO, OutputDTO](Protocol):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
InteractorFactory = Callable[[], InteractorT]


class EventHandler[E: BaseEvent, OutputDTO](Interactor[E, OutputDTO], Protocol):
    broker: Broker

    @abstractmethod
    async def __call__(self, event: E) -> OutputDTO:
        raise NotImplementedError
