from src.diary_ms.domain.model.entities.medicament import MedicamentId
from src.diary_ms.domain.model.entities.user_id import UserId


class CreateMedicamentCommand:
    user_id: UserId
    name: str
    dosage: str

    id: MedicamentId | None = None
