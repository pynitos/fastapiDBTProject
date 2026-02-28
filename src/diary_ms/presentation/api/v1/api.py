from fastapi import FastAPI

from diary_ms.main.config import web_config
from diary_ms.presentation.api.constants.enums import Prefix, Tags
from diary_ms.presentation.api.exceptions import include_exception_handlers

from ..deps import TokenDep
from .controllers import diary_cards, medicaments, target_behavior

api_v1 = FastAPI(
    title=web_config.PROJECT_NAME,
    description="",
    version="1.0",
    dependencies=[TokenDep],
)
include_exception_handlers(api_v1)

api_v1.include_router(
    diary_cards.router,
    prefix=Prefix.DIARY_CARDS,
    tags=[Tags.DIARY_CARDS],
)

api_v1.include_router(
    medicaments.router,
    prefix=Prefix.MEDICAMENTS,
    tags=[Tags.MEDICAMENTS],
)

api_v1.include_router(
    target_behavior.router,
    prefix=Prefix.TARGETS,
    tags=[Tags.TARGETS],
)
