from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class DiaryCardAdminSaver(Protocol):
    @abstractmethod
    async def create(self, entity: DiaryCard) -> None:
        raise NotImplementedError


class DiaryCardAdminReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCard]:
        raise NotImplementedError


class DiaryCardDTOForUpdateAdminReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId) -> DiaryCard | None:
        raise NotImplementedError


class DiaryCardAdminUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: DiaryCard) -> None:
        raise NotImplementedError


class DiaryCardAdminDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: DiaryCardId) -> None:
        raise NotImplementedError
