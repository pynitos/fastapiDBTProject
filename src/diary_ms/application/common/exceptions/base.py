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


class ItemIdNotProvidedError(GatewayError):
    _detail: str = "Item Id Not Provided."


class MediatorError(ApplicationError):
    pass


class MappingError(ApplicationError):
    pass


class HandlerNotFoundError(MediatorError):
    pass
