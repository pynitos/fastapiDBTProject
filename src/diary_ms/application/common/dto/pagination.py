from dataclasses import dataclass

from src.diary_ms.application.common.dto.base import DTO

PAGE_SIZE = 10


@dataclass
class Pagination(DTO):
    limit: int = PAGE_SIZE
    offset: int = 0
