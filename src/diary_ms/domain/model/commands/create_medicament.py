from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class CreateMedicamentCommand:
    user_id: UserId
    name: str
    dosage: str

    id: MedicamentId | None = None
