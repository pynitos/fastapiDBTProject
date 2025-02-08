from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class TargetAdminSaver(Protocol):
    @abstractmethod
    async def create(self, entity: Target) -> None:
        raise NotImplementedError


class TargetAdminReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: TargetId) -> Target | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Target]:
        raise NotImplementedError


class TargetAdminUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: TargetId) -> Target | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Target) -> None:
        raise NotImplementedError


class TargetAdminDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: TargetId) -> None:
        raise NotImplementedError
