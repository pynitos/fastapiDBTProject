from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteDiaryCardCommand:
    id: UUID
