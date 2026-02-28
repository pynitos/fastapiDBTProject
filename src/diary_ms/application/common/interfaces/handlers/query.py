from abc import abstractmethod
from typing import Any, Protocol, TypeVar

from diary_ms.application.common.dto.query import Query
from diary_ms.application.common.interfaces.handlers.base import Handler

QT = TypeVar("QT", bound=Query[Any], contravariant=True)
QR = TypeVar("QR", covariant=True)


class QueryHandler(Handler[QT, QR], Protocol):
    @abstractmethod
    async def __call__(self, query: QT) -> QR:
        raise NotImplementedError
