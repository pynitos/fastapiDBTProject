from types import MappingProxyType
from typing import Final

from src.diary_ms.infrastructure.error_code import ErrorCode


class ErrorMessage:
    def __init__(self) -> None:
        self._msg: Final[MappingProxyType[ErrorCode, str]] = MappingProxyType(
            {
                ErrorCode.GATEWAY_ERROR: "Unknown Error!",
                ErrorCode.DIARY_CARD_NOT_FOUND: "Diary card not found!",
            },
        )

    def get_error_message(self, error_code: ErrorCode) -> str:
        return self._msg[error_code]
