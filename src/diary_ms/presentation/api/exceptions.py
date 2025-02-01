import logging
from collections.abc import Awaitable, Callable
from functools import partial
from typing import Any

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from src.diary_ms.application.common.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.domain.common.exceptions.base import AppError, DomainValueError
from src.diary_ms.presentation.api.responses.base import ErrorData, ErrorResponse

# from src.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError, UsernameNotExistError
# from src.domain.common.exceptions import AppError
# from src.domain.user.exceptions import UserIsDeletedError, UsernameAlreadyExistsError
# from src.domain.user.value_objects.full_name import WrongNameValueError
# from src.domain.user.value_objects.username import WrongUsernameValueError
# from src.presentation.api.controllers.responses import ErrorResponse
# from src.presentation.api.controllers.responses.base import ErrorData
# from src.presentation.api.controllers.responses.orjson import ORJSONResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, error_handler(AppError.get_status_code()))
    app.add_exception_handler(DiaryCardNotFoundError, error_handler(DiaryCardNotFoundError.get_status_code()))
    app.add_exception_handler(DomainValueError, error_handler(DomainValueError.get_status_code()))
    # app.add_exception_handler(WrongUsernameValueError, error_handler(status.HTTP_400_BAD_REQUEST))
    # app.add_exception_handler(WrongNameValueError, error_handler(status.HTTP_400_BAD_REQUEST))
    # app.add_exception_handler(UserIdAlreadyExistsError, error_handler(status.HTTP_409_CONFLICT))
    # app.add_exception_handler(UsernameAlreadyExistsError, error_handler(status.HTTP_409_CONFLICT))
    # app.add_exception_handler(UserIsDeletedError, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(request: Request, err: AppError, status_code: int) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(title=err.detail, data=err),
        status_code=err.status_code,
    )


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:  # noqa: ARG001
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,  # noqa: ARG001
    err: Exception,
    err_data: ErrorData[Any],
    status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status_code),
        status_code=status_code,
    )
