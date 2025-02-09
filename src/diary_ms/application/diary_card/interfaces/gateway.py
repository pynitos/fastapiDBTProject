from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.user_id import UserId


class DiaryCardSaver(Protocol):
    @abstractmethod
    async def create(self, entity: DiaryCard) -> None:
        raise NotImplementedError


class DiaryCardReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId, user_id: UserId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, user_id: UserId, offset: int = 0, limit: int = 10) -> list[DiaryCard]:
        raise NotImplementedError


class DiaryCardUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: DiaryCardId, user_id: UserId) -> DiaryCard | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: DiaryCard) -> None:
        raise NotImplementedError


class DiaryCardDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: DiaryCardId, user_id: UserId) -> None:
        raise NotImplementedError


class EmotionReader(Protocol):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Emotion]:
        raise NotImplementedError


class SkillReader(Protocol):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Skill]:
        raise NotImplementedError
