from dataclasses import dataclass
from uuid import UUID


@dataclass
class EmotionAdminDTO:
    id: UUID
    user_id: UUID
    name: str
    description: str | None
