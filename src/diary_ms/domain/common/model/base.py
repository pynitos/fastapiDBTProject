from dataclasses import dataclass
from datetime import datetime

from ..types.id import TypeId


@dataclass
class BaseDM:
    id: TypeId
    created_at: datetime
    updated_at: datetime
