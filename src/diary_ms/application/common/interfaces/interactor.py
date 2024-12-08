from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol, TypeVar

from src.diary_ms.domain.common.model.events.base import BaseEvent


class Interactor[InputDTO, OutputDTO](Protocol):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
InteractorFactory = Callable[[], InteractorT]


class QueryHandler[QT, QR](Protocol):
    @abstractmethod
    async def __call__(self, query: QT) -> QR:
        raise NotImplementedError


class CommandHandler[CT, CR](Protocol):
    @abstractmethod
    async def __call__(self, command: CT) -> CR:
        raise NotImplementedError


class EventHandler[ET: BaseEvent, ER](Protocol):
    @abstractmethod
    async def __call__(self, event: ET) -> ER:
        raise NotImplementedError
