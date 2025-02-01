from src.diary_ms.domain.common.exceptions.base import AppError


class ApplicationError(AppError):
    pass


class InfraError(AppError):
    pass


class GatewayError(InfraError):
    pass


class ItemNotFoundError(GatewayError):
    _detail: str = "Item Not Found."
    _status_code: int = 404


class MediatorError(ApplicationError):
    pass


class HandlerNotFoundError(MediatorError):
    _detail: str = "Command or query handler not registered."
