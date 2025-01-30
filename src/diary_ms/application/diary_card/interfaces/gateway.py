from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from src.diary_ms.application.diary_card.dto.diary_card import OwnDiaryCardDTO
from src.diary_ms.application.diary_card.dto.for_update_diary_card import (
    DiaryCardForUpdateDTO,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import Emotion


class DiaryCardSaver(Protocol):
    @abstractmethod
    async def create(self, entity: DiaryCard) -> None:
        raise NotImplementedError


class DiaryCardReader(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: DiaryCardId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCard]:
        raise NotImplementedError


class DiaryCardDTOForUpdateReader(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: DiaryCardId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def get_dto_for_update(self, id: DiaryCardId) -> DiaryCardForUpdateDTO:
        raise NotImplementedError


class DiaryCardUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: DiaryCard) -> None:
        raise NotImplementedError


class DiaryCardDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: DiaryCardId) -> None:
        raise NotImplementedError


class EmotionReader(Protocol):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> Sequence[Emotion]:
        raise NotImplementedError
