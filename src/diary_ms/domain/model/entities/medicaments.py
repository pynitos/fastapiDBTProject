from src.diary_ms.domain.common.model.base import BaseDM
from src.diary_ms.domain.model.entities.user_id import UserId


class Medicament(BaseDM):
    user_id: UserId
    name: str
    dosage: str

