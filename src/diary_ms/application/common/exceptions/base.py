from src.diary_ms.domain.common.exceptions.base import AppError


class ApplicationError(AppError):
    pass


class InfraError(AppError):
    pass


class GatewayError(InfraError):
    pass


class ItemNotFoundError(GatewayError):
    pass
