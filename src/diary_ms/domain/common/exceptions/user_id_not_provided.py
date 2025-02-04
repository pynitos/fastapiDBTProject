from src.diary_ms.domain.common.exceptions.base import DomainError


class UserIdNotProvidedError(DomainError):
    _detail: str = "User Id Not Provided"
