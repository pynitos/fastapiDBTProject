from enum import Enum

from src.diary_ms.application.common.exceptions.base import GatewayError, ItemNotFoundError
from src.diary_ms.application.common.exceptions.diary_card import DiaryCardNotFoundError


class ErrorCode(Enum):
    GATEWAY_ERROR = GatewayError
    ITEM_NOT_FOUND_ERROR = ItemNotFoundError
    DIARY_CARD_NOT_FOUND = DiaryCardNotFoundError
