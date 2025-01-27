from fastapi import FastAPI

from src.diary_ms.presentation.api.constants.enums import Tags
from src.diary_ms.presentation.api.deps import TokenDep

from .routes.admin import emotions, skills

admin_api_v1 = FastAPI(
    title="Admin Panel API: Diary Cards.", description="API for admins.", version="1.0", dependencies=[TokenDep]
)

admin_api_v1.include_router(
    emotions.router,
    prefix="/emotions",
    tags=[Tags.EMOTIONS],
)

admin_api_v1.include_router(
    skills.router,
    prefix="/skills",
    tags=[Tags.SKILLS],
)
