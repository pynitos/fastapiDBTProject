from abc import abstractmethod
from typing import Any, Protocol

TDependency = Any


class Resolver(Protocol):
    @abstractmethod
    async def resolve(
        self,
        dependency_type: type[TDependency],
    ) -> TDependency: ...
