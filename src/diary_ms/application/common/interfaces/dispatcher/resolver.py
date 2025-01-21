from abc import abstractmethod
from typing import Protocol, TypeVar

TDependency = TypeVar("TDependency")


class Resolver(Protocol):
    @abstractmethod
    async def resolve(
        self,
        dependency_type: type[TDependency],
    ) -> TDependency: ...
