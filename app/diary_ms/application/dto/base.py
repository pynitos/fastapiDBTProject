from dataclasses import dataclass

from app.diary_ms.domain.models.id import Id


@dataclass
class BaseDTO:
    id: Id
