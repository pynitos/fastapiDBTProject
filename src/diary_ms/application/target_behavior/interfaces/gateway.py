from abc import abstractmethod
from typing import Protocol

from diary_ms.domain.model.entities.target_behavior import Target
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class TargetSaver(Protocol):
    @abstractmethod
    async def create(self, entity: Target) -> None:
        raise NotImplementedError


class TargetReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: TargetId, user_id: UserId) -> Target | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Target]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_own(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Target]:
        raise NotImplementedError

    @abstractmethod
    async def get_total_count(self, user_id: UserId) -> int:
        raise NotImplementedError


class TargetUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: TargetId, user_id: UserId) -> Target | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Target) -> None:
        raise NotImplementedError


class TargetDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: TargetId, user_id: UserId) -> None:
        raise NotImplementedError
