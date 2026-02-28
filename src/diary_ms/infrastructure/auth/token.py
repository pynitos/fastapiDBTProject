import logging
import uuid
from collections.abc import Iterable, Sequence
from datetime import timedelta
from typing import Any, Literal

import jwt

from diary_ms.application.common.interfaces.id_provider import IdProvider
from diary_ms.domain.common.exceptions.access import AuthenticationError
from diary_ms.domain.model.entities.user_id import UserId

logger = logging.getLogger(__name__)

AlgorithmT = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]


class JwtTokenProcessor:
    def __init__(
        self,
        secret: str,
        expires: timedelta,
        algorithm: AlgorithmT,
        audience: str | Iterable[str] | None = None,
        issuer: str | Sequence[str] | None = None,
        leeway: float | timedelta = 0,
    ) -> None:
        self.secret = secret
        self.expires = expires
        self.algorithm = algorithm

        self.audience = audience
        self.issuer = issuer
        self.leeway = leeway

    def validate_token(self, token: str, verify: bool = True) -> dict[str, Any]:
        try:
            payload: dict[str, Any] = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                leeway=self.leeway,
                options={
                    "verify_aud": self.audience is not None,
                    "verify_signature": verify,
                },
            )
            return payload
        except jwt.PyJWTError as e:
            logger.debug(e)
            raise AuthenticationError

    def authorize_user(self, token: str) -> uuid.UUID:
        payload: dict[str, Any] = self.validate_token(token)
        try:
            return uuid.UUID(payload["sub"])
        except (ValueError, KeyError) as e:
            logger.debug(e)
            raise AuthenticationError

    def authorize_admin(self, token: str) -> uuid.UUID:
        payload: dict[str, Any] = self.validate_token(token)
        try:
            return uuid.UUID(payload["sub"])
        except (ValueError, KeyError) as e:
            logger.debug(e)
            raise AuthenticationError


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token_processor: JwtTokenProcessor,
        token: str,
    ) -> None:
        self.token_processor = token_processor
        self.token = token

    def get_current_user_id(self) -> UserId:
        id: uuid.UUID = self.token_processor.authorize_user(self.token)
        return UserId(id)
