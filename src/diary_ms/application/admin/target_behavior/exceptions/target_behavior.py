from src.diary_ms.application.common.exceptions.base import GatewayError, ItemNotFoundError
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId


class TargetNotFoundAdminError(ItemNotFoundError):
    _detail: str = "Target Not Found!"
    _status_code: int = 404

    def __init__(self, id: TargetId, status_code: int = 404):
        if id.value:
            detail: str = f"Target with id: {str(id.value)} not found!"
            super().__init__(detail, status_code)
        super().__init__(status_code=status_code)


class TargetIdNotProvidedAdminError(GatewayError):
    _detail: str = "Target Id Not Provided!"
