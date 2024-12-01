from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.diary_ms.application.dto.diary_card import OwnDiaryCardDTO
from src.diary_ms.application.dto.for_update_diary_card import DiaryCardForUpdateDTO
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


class SaverProtocol(Protocol):
    @abstractmethod
    async def create(self, entity: DiaryCardDM) -> None:
        raise NotImplementedError


class ReaderProtocol(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: DiaryCardId) -> DiaryCardDM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[OwnDiaryCardDTO]:
        raise NotImplementedError


class DTOReader(Protocol):
    @abstractmethod
    async def get_dto_by_id(self, id: DiaryCardId) -> OwnDiaryCardDTO | None:
        raise NotImplementedError


class DTOForUpdateReader(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: DiaryCardId) -> DiaryCardDM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_dto_for_update(self, dm: DiaryCardDM) -> DiaryCardForUpdateDTO:
        raise NotImplementedError


class UpdaterProtocol(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: UUID) -> DiaryCardDM | None:
        pass

    @abstractmethod
    async def update(self, entity: DiaryCardDM) -> None:
        pass


class DeleterProtocol(Protocol):
    @abstractmethod
    async def delete(self, id: DiaryCardId) -> None:
        pass
