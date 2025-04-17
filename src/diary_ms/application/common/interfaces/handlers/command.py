from abc import abstractmethod
from typing import Any, Protocol, TypeVar

from src.diary_ms.application.common.dto.base import ResultDTO
from src.diary_ms.application.common.dto.command import Command
from src.diary_ms.application.common.interfaces.handlers.base import Handler

CT = TypeVar("CT", bound=Command[Any], contravariant=True)
CR = TypeVar("CR", bound=ResultDTO | None, covariant=True)


class CommandHandler(Handler[CT, CR], Protocol):
    @abstractmethod
    async def __call__(self, command: CT) -> CR:
        raise NotImplementedError
