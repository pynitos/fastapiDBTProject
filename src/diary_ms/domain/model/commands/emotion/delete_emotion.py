from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteEmotionAdminCommand:
    id: UUID
