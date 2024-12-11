from abc import abstractmethod
from typing import Protocol, TypeVar

from src.diary_ms.application.common.interfaces.handlers.base import Handler

QT = TypeVar("QT", contravariant=True)
QR = TypeVar("QR", covariant=True)


class QueryHandler(Handler[QT, QR], Protocol[QT, QR]):
    @abstractmethod
    async def __call__(self, query: QT) -> QR:
        raise NotImplementedError


QueryHandlerType = QueryHandler[QT, QR]
