from abc import abstractmethod
from asyncio import Protocol
from uuid import UUID

from sqlmodel import SQLModel


class SaverProtocol[TModel: SQLModel](Protocol):
    @abstractmethod
    async def create(self, entity: TModel) -> None:
        ...


class ReaderProtocol[TDModel: SQLModel](Protocol):
    @abstractmethod
    async def get_by_id(self, pk: UUID) -> TDModel | None:
        ...

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 10) -> list[TDModel]:
        ...
