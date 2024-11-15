from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from src.diary_ms.domain.common.types.id import TypeId


@dataclass
class BaseEntity(ABC):
    id: TypeId

