import logging

from dishka import AnyOf, Provider, Scope, provide
from fastapi import HTTPException, Request

from src.diary_ms.application.common.interfaces.id_provider import (
    AdminIdProvider,
    IdProvider,
)
from src.diary_ms.infrastructure.auth.token import JwtTokenProcessor, TokenIdProvider

logger = logging.getLogger(__name__)


class AdaptersFastapiProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_id_provider(
        self,
        token_processor: JwtTokenProcessor,
        request: Request,
    ) -> AnyOf[IdProvider, AdminIdProvider, TokenIdProvider]:
        auth_header: str | None = request.headers.get("AUTHORIZATION")
        if not auth_header:
            raise HTTPException(401, "Unauthorized.")
        jwt_token: str = auth_header.split("Bearer ")[-1]
        return TokenIdProvider(
            token_processor=token_processor,
            token=jwt_token,
        )
