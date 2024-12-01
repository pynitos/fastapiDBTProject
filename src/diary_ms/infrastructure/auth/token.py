import uuid
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from jose import JWTError, jwt

from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.domain.common.exceptions.access import AuthenticationError
from src.diary_ms.domain.model.entities.user_id import UserId

Algorithm = Literal[
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
        algorithm: Algorithm,
    ) -> None:
        self.secret = secret
        self.expires = expires
        self.algorithm = algorithm

    def create_access_token(
        self,
        user_id: UserId,
    ) -> str:
        to_encode: dict[str, Any] = {"sub": str(user_id)}
        expire = datetime.now(UTC) + self.expires
        to_encode["exp"] = expire
        return jwt.encode(
            to_encode,
            self.secret,
            algorithm=self.algorithm,
        )

    def validate_token(self, token: str) -> uuid.UUID:
        try:
            payload: dict[str, Any] = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
            )
        except JWTError:
            raise AuthenticationError

        try:
            return uuid.UUID(payload["sub"])
        except ValueError:
            raise AuthenticationError


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token_processor: JwtTokenProcessor,
        token: str,
    ):
        self.token_processor = token_processor
        self.token = token

    def get_current_user_id(self) -> uuid.UUID:
        return self.token_processor.validate_token(self.token)


class FakeIdProvider(IdProvider):
    def get_current_user_id(self) -> uuid.UUID:
        return uuid.uuid4()
