from fastapi import FastAPI

from src.diary_ms.main.config import settings

from ..deps import TokenDep
from .admin import admin_api_v1
from .routes import diary_cards

api_v1 = FastAPI(title=settings.PROJECT_NAME, description="", version="1.0")

api_v1.mount("/admin", admin_api_v1)

api_v1.include_router(
    diary_cards.router,
    tags=["diary_cards"],
    dependencies=[
        TokenDep,
    ],
)
