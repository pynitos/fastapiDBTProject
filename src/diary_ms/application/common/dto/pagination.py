from dataclasses import dataclass

from diary_ms.application.common.dto.base import ResultDTO

PAGE_SIZE = 10


@dataclass
class Pagination(ResultDTO):
    limit: int = PAGE_SIZE
    offset: int = 0
