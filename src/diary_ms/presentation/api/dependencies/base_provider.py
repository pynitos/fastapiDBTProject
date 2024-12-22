from dishka import Provider, Scope, provide
from fastapi import HTTPException, Request

from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.infrastructure.auth.token import JwtTokenProcessor, TokenIdProvider


class AdaptersFastapiProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_id_provider(
        self,
        token_processor: JwtTokenProcessor,
        request: Request,
    ) -> IdProvider:
        auth_header: str | None = request.headers.get("AUTHORIZATION")
        if not auth_header:
            raise HTTPException(401, "Unauthorized.")
        jwt_token: str = auth_header.split("Bearer")[-1]
        return TokenIdProvider(
            token_processor=token_processor,
            token=jwt_token,
        )
