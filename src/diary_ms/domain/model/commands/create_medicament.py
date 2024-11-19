from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateMedicamentCommand:
    name: str
    dosage: str
    id: UUID | None = None
    user_id: UUID | None = None
