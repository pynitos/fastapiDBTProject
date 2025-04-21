from abc import abstractmethod
from typing import Protocol

from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from src.diary_ms.domain.model.value_objects.skill.type import SkillType


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

    @abstractmethod
    async def get_total_count(
        self, user_id: UserId, date_from: DCDateOfEntry | None = None, date_to: DCDateOfEntry | None = None
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def generate_report_data(
        self,
        user_id: UserId,
        start_date: DCDateOfEntry,
        end_date: DCDateOfEntry,
    ) -> DiaryCardsReportDTO:
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
    async def get_all(self, type: SkillType, offset: int = 0, limit: int = 10) -> list[Skill]:
        raise NotImplementedError
