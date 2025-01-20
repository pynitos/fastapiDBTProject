from abc import abstractmethod
from typing import Protocol

from src.diary_ms.application.diary_card.dto.diary_card import OwnDiaryCardDTO
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard


class DiaryCardDTOMapper(Protocol):
    @staticmethod
    @abstractmethod
    def dm_to_dto(dm: DiaryCard) -> OwnDiaryCardDTO:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def dm_list_to_dto_list(cls, dm_list: list[DiaryCard]) -> list[OwnDiaryCardDTO]:
        raise NotImplementedError
