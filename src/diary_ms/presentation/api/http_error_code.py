from types import MappingProxyType
from typing import Final

from src.diary_ms.infrastructure.error_code import ErrorCode

HTTP_ERROR_CODE: Final[MappingProxyType[ErrorCode, int]] = MappingProxyType(
    {
        ErrorCode.DIARY_CARD_NOT_FOUND: 404,
    },
)
