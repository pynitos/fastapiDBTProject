from typing import Annotated

from fastapi import Cookie

from src.diary_ms.application.interfaces.id_provider import IdProvider
from src.diary_ms.infrastructure.auth.token import (
    JwtTokenProcessor,
    TokenIdProvider,
)


def get_id_provider(
    token_processor: JwtTokenProcessor,
    token: Annotated[str, Cookie()],
) -> IdProvider:
    return TokenIdProvider(
        token_processor=token_processor,
        token=token,
    )
