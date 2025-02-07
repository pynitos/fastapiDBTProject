from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class MedicamentAdminSaver(Protocol):
    @abstractmethod
    async def create(self, entity: Medicament) -> None:
        raise NotImplementedError


class MedicamentAdminReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: MedicamentId, user_id: UserId) -> Medicament | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[Medicament]:
        raise NotImplementedError


class MedicamentAdminUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: MedicamentId, user_id: UserId) -> Medicament | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Medicament) -> None:
        raise NotImplementedError


class MedicamentAdminDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: MedicamentId, user_id: UserId) -> None:
        raise NotImplementedError
