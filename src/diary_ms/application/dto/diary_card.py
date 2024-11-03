from dataclasses import dataclass

from src.diary_ms.application.dto.pagination import Pagination


@dataclass
class DiaryCardDTO:
    description: str


@dataclass
class NewDiaryCardDTO:
    description: str


@dataclass
class GetOwnDiaryCardsDTO:
    pagination: Pagination



