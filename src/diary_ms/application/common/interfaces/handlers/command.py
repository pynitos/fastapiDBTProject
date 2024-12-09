from abc import abstractmethod
from typing import Protocol, TypeVar

from src.diary_ms.application.common.interfaces.handlers.base import Handler

CT = TypeVar("CT", contravariant=True)
CR = TypeVar("CR", covariant=True)


class CommandHandler(Handler[CT, CR], Protocol[CT, CR]):
    @abstractmethod
    async def __call__(self, command: CT) -> CR:
        raise NotImplementedError


CommandHandlerType = type[CommandHandler[CT, CR]] | CommandHandler[CT, CR]
