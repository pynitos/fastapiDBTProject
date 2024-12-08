from src.diary_ms.domain.common.exceptions.base import AppError


class ApplicationError(AppError):
    pass


class InfraError(AppError):
    pass


class GatewayError(InfraError):
    pass


class ItemNotFoundError(GatewayError):
    pass


class MediatorError(ApplicationError):
    pass


class CommandHandlersNotRegisteredError(MediatorError):
    _detail: str = "Command handlers not registered."
