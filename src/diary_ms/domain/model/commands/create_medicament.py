from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateMedicamentCommand:
    name: str
    dosage: str
    user_id: UUID
    id: UUID | None = None
