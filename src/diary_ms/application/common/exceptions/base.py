from src.diary_ms.domain.common.exceptions.base import AppError


class ApplicationError(AppError):
    pass


class GatewayError(ApplicationError):
    pass


class ItemNotFoundError(GatewayError):
    pass
