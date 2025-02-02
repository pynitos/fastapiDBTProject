import logging

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from src.diary_ms.domain.common.exceptions.base import AppError

logger = logging.getLogger(__name__)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_exception_handler)
    logging.info("Exception handlers was included.")


async def get_http_error_response(
    err: AppError,  # noqa: F821
) -> ORJSONResponse:
    logger.debug("Handle error.", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        status_code=err.status_code,
        content={
            "error_code": err.status_code,
            "message": err.detail,
        },
    )


async def app_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:  # noqa: ARG001
    if not isinstance(exc, AppError):
        logger.error("Handle error.", exc_info=exc, extra={"error": exc})
        logger.exception("Unknown error occurred.", exc_info=exc, extra={"error": exc})
        return ORJSONResponse("Unknown error occurred.", 500)

    return await get_http_error_response(exc)
