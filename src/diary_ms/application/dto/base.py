from dataclasses import dataclass

from src.diary_ms.domain.model.entities import Id


@dataclass
class BaseDTO:
    id: Id
