import dataclasses

from datetime import datetime
from uuid import UUID


@dataclasses.dataclass
class BaseDM:
    id: UUID
    created_at: datetime
    updated_at: datetime
