import logging

from dishka import AnyOf, Provider, Scope, provide
from fastapi import Request

from diary_ms.application.common.interfaces.id_provider import (
    AdminIdProvider,
    IdProvider,
)
from diary_ms.domain.common.exceptions.access import AuthenticationError
from diary_ms.infrastructure.auth.token import JwtTokenProcessor, TokenIdProvider

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
        logger.info("User id provider running.")
        if not auth_header:
            raise AuthenticationError("Unautenticated. Authorization header is empty.", 401)
        jwt_token: str = auth_header.split("Bearer ")[-1]
        return TokenIdProvider(
            token_processor=token_processor,
            token=jwt_token,
        )
