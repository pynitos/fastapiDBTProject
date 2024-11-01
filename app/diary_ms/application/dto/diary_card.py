from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from app.diary_ms.application.dto.pagination import Pagination
from app.diary_ms.domain.models.diary_card import DiaryCardDM


@dataclass
class DiaryCardDTO:
    description: str


@dataclass
class NewDiaryCardDTO:
    description: str


@dataclass
class GetOwnDiaryCardsDTO:
    pagination: Pagination



