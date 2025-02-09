from src.diary_ms.application.common.exceptions.base import GatewayError, ItemNotFoundError
from src.diary_ms.domain.model.value_objects.skill.id import SkillId


class SkillNotFoundError(ItemNotFoundError):
    _detail: str = "Target Not Found!"
    _status_code: int = 404

    def __init__(self, id: SkillId, status_code: int = 404):
        if id.value:
            detail: str = f"Skill with id: {str(id.value)} not found!"
            super().__init__(detail, status_code)
        super().__init__(status_code=status_code)


class SkillIdNotProvidedError(GatewayError):
    _detail: str = "Skill Id Not Provided!"
