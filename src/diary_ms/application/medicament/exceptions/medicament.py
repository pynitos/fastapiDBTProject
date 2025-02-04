from src.diary_ms.application.common.exceptions.base import GatewayError, ItemNotFoundError
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId


class MedicamentNotFoundError(ItemNotFoundError):
    _detail: str = "Medicament Not Found!"
    _status_code: int = 404

    def __init__(self, id: MedicamentId, status_code: int = 404):
        if id.value:
            detail: str = f"Medicament with id: {id} not found!"
            super().__init__(detail, status_code)
        super().__init__()


class MedicamentIdNotProvidedError(GatewayError):
    _detail: str = "Medicament Id Not Provided!"
