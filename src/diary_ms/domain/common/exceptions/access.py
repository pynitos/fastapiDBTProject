from .base import DomainError


class AuthenticationError(DomainError):
    _status_code: int = 401
    _detail: str = "Authentication Error."


class AccessDenied(DomainError):
    pass
