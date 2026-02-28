from abc import abstractmethod
from typing import Protocol

from diary_ms.application.diary_card.dto.diary_card import OwnDiaryCardResultDTO
from diary_ms.domain.model.aggregates.diary_card import DiaryCard


class DiaryCardDTOMapper(Protocol):
    @classmethod
    @abstractmethod
    def dm_to_dto(cls, dm: DiaryCard) -> OwnDiaryCardResultDTO:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def dm_list_to_dto_list(cls, dm_list: list[DiaryCard]) -> list[OwnDiaryCardResultDTO]:
        raise NotImplementedError
