from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateEmotionCommand:
    name: str
    description: str | None = None
    user_id: UUID | None = None
