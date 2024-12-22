from abc import abstractmethod
from typing import Protocol

from src.diary_ms.application.diary_card.dto.diary_card import OwnDiaryCardDTO
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    DiaryCardForUpdateDTO,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class DiaryCardSaver(Protocol):
    @abstractmethod
    async def create(self, entity: DiaryCardDM) -> None:
        raise NotImplementedError


class DiaryCardReader(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: DiaryCardId) -> DiaryCardDM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[OwnDiaryCardDTO]:
        raise NotImplementedError


class DiaryCardDTOReader(Protocol):
    @abstractmethod
    async def get_dto_by_id(self, id: DiaryCardId) -> OwnDiaryCardDTO | None:
        raise NotImplementedError


class DiaryCardDTOForUpdateReader(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: DiaryCardId) -> DiaryCardDM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_dto_for_update(self, dm: DiaryCardDM) -> DiaryCardForUpdateDTO:
        raise NotImplementedError


class DiaryCardUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId) -> DiaryCardDM | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: DiaryCardDM) -> None:
        raise NotImplementedError


class DiaryCardDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: DiaryCardId) -> None:
        raise NotImplementedError
