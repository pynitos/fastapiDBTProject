import logging

from dishka import AsyncContainer
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.infrastructure.error_code import ErrorCode
from src.diary_ms.presentation.api.http_error_code import HTTP_ERROR_CODE
from src.diary_ms.presentation.error_message import ErrorMessage

logger = logging.getLogger(__name__)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_exception_handler)
    logging.info("Exception handlers was included.")


def get_http_error_response(
    err: AppError,  # noqa: F821
    error_message: ErrorMessage,
) -> ORJSONResponse:
    err_type = type(err)
    err_code = ErrorCode(err_type)
    err_message = error_message.get_error_message(err_code)
    err_http_code = HTTP_ERROR_CODE[ErrorCode(err_type)]

    return ORJSONResponse(
        status_code=err_http_code,
        content={
            "error_code": err_code.name,
            "message": err_message,
        },
    )


async def app_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    if not isinstance(exc, AppError):
        logger.error("Handle error.", exc_info=exc, extra={"error": exc})
        logger.exception("Unknown error occurred.", exc_info=exc, extra={"error": exc})
        return ORJSONResponse("Unknown error occurred.", 500)

    di_container: AsyncContainer = request.state.dishka_container
    error_message = await di_container.get(ErrorMessage)

    return get_http_error_response(exc, error_message)
