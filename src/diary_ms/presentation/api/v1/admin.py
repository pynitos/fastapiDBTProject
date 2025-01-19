from fastapi import FastAPI

from ..deps import TokenDep
from .routes.admin import emotions

admin_api_v1 = FastAPI(title="Admin Panel API: Diary Cards.", description="API for admins.", version="1.0")

admin_api_v1.include_router(
    emotions.router,
    prefix="/emotions",
    tags=["admin"],
    dependencies=[
        TokenDep,
    ],
)
