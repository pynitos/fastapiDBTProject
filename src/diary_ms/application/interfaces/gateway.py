from abc import abstractmethod
from asyncio import Protocol

from src.diary_ms.domain.common.types.id import TypeId


class SaverProtocol[TModel](Protocol):
    @abstractmethod
    def create(self, entity: TModel) -> None:
        ...


class UpdaterProtocol[TModel](Protocol):
    @abstractmethod
    async def update(self, pk: TypeId, entity: TModel) -> None:
        ...


class ReaderProtocol[TDModel](Protocol):
    @abstractmethod
    async def get_by_id(self, pk: TypeId) -> TDModel | None:
        ...

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 10) -> list[TDModel]:
        ...


class DeleterProtocol(Protocol):
    @abstractmethod
    async def delete(self, id: TypeId) -> None:
        ...
