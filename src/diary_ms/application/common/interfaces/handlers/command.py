from abc import abstractmethod
from typing import Protocol, TypeVar

from src.diary_ms.application.common.dto.base import DTO
from src.diary_ms.application.common.interfaces.handlers.base import Handler
from src.diary_ms.domain.common.model.commands.base import Command

CT = TypeVar("CT", bound=Command, contravariant=True)
CR = TypeVar("CR", bound=DTO | None, covariant=True)


class CommandHandler(Handler[CT, CR], Protocol[CT, CR]):
    @abstractmethod
    async def __call__(self, command: CT) -> CR:
        raise NotImplementedError
