import os
import warnings
from dataclasses import dataclass, field
from typing import Any, Literal

from dotenv import load_dotenv

from src.diary_ms.infrastructure.auth.token import AlgorithmT
from src.diary_ms.infrastructure.s3.config import S3Config


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


@dataclass
class BaseConfig:
    def post_init(self):
        self._validate()

    def _validate(self):
        pass


@dataclass
class WebConfig(BaseConfig):
    s3: S3Config
    DB_URI: str
    BROKER_URI: str
    REDIS_URI: str
    JWT_SECRET_KEY: str
    API_PREFIX: str = "/api"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_ALGORITHM: AlgorithmT = "HS256"
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: list[str] | str = field(default_factory=list)
    PROJECT_NAME: str = "Diary card API"
    SENTRY_DSN: str | None = None

    def _validate(self):
        parse_cors(self.BACKEND_CORS_ORIGINS)

    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", ' "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)


def load_web_config() -> WebConfig:
    load_dotenv()
    db_uri = os.environ["DB_URI"]
    broker_uri = os.environ["BROKER_URI"]
    redis_uri = os.environ["REDIS_URI"]
    jwt_secret_key = os.environ["JWT_SECRET_KEY"]
    s3 = S3Config(
        endpoint_url=os.environ["MINIO_URL"],
        aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
        aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
    )
    return WebConfig(
        s3=s3,
        DB_URI=db_uri,
        BROKER_URI=broker_uri,
        REDIS_URI=redis_uri,
        JWT_SECRET_KEY=jwt_secret_key,
    )


web_config: WebConfig = load_web_config()
