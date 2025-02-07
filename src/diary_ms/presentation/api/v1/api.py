from fastapi import FastAPI

from src.diary_ms.main.config import settings
from src.diary_ms.presentation.api.constants.enums import Prefix, Tags
from src.diary_ms.presentation.api.exceptions import include_exception_handlers

from ..deps import TokenDep
from .admin import admin_api_v1
from .controllers import diary_cards, emotions, medicaments

api_v1 = FastAPI(
    title=settings.PROJECT_NAME,
    description="",
    version="1.0",
    dependencies=[TokenDep],
)
include_exception_handlers(api_v1)
api_v1.mount(Prefix.ADMIN, admin_api_v1)

api_v1.include_router(
    diary_cards.router,
    prefix=Prefix.DIARY_CARDS,
    tags=[Tags.DIARY_CARDS],
)

api_v1.include_router(
    emotions.router,
    prefix=Prefix.EMOTIONS,
    tags=[Tags.EMOTIONS],
)

api_v1.include_router(
    medicaments.router,
    prefix=Prefix.MEDICAMENTS,
    tags=[Tags.MEDICAMENTS],
)
