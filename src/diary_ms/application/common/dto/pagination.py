from dataclasses import dataclass

from src.diary_ms.application.common.dto.base import DTO


@dataclass
class Pagination(DTO):
    limit: int
    offset: int
