from fastapi import Cookie
from typing_extensions import Annotated

from src.diary_ms.adapters.auth.token import (
    JwtTokenProcessor, TokenIdProvider,
)
from src.diary_ms.application.interfaces.id_provider import IdProvider


def get_id_provider(
        token_processor: JwtTokenProcessor,
        token: Annotated[str, Cookie()],
) -> IdProvider:
    return TokenIdProvider(
        token_processor=token_processor,
        token=token,
    )
