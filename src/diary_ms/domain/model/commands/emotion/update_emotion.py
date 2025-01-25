from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateEmotionAdminCommand:
    id: UUID
    name: str | None = None
    description: str | None = None
