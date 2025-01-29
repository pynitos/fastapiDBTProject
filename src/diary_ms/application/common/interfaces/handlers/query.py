from abc import abstractmethod
from typing import Protocol, TypeVar

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.dto.query import Query
from src.diary_ms.application.common.interfaces.handlers.base import Handler

QT = TypeVar("QT", bound=Query, contravariant=True)
QR = TypeVar("QR", bound=DTO | None, covariant=True)


class QueryHandler(Handler[QT, QR], Protocol):
    @abstractmethod
    async def __call__(self, query: QT) -> QR:
        raise NotImplementedError
