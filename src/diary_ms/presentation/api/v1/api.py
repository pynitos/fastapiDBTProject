from fastapi import FastAPI

from src.diary_ms.main.config import settings
from src.diary_ms.presentation.api.constants.enums import Tags
from src.diary_ms.presentation.api.exceptions import include_exception_handlers

from ..deps import TokenDep
from .admin import admin_api_v1
from .routes import diary_cards, emotions

api_v1 = FastAPI(
    title=settings.PROJECT_NAME,
    description="",
    version="1.0",
    dependencies=[TokenDep],
)
include_exception_handlers(api_v1)
api_v1.mount("/admin", admin_api_v1)

api_v1.include_router(
    diary_cards.router,
    tags=[Tags.DIARY_CARDS],
)

api_v1.include_router(
    emotions.router,
    prefix="/emotions",
    tags=[Tags.EMOTIONS],
)
