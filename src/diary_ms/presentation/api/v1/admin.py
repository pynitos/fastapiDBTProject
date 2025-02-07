from fastapi import FastAPI

from src.diary_ms.presentation.api.constants.enums import Prefix, Tags
from src.diary_ms.presentation.api.deps import TokenDep
from src.diary_ms.presentation.api.exceptions import include_exception_handlers

from .controllers.admin import emotions, medicaments, skills

admin_api_v1 = FastAPI(
    title="Admin Panel API: Diary Cards.", description="API for admins.", version="1.0", dependencies=[TokenDep]
)
include_exception_handlers(admin_api_v1)

admin_api_v1.include_router(
    emotions.router,
    prefix=Prefix.EMOTIONS,
    tags=[Tags.EMOTIONS],
)

admin_api_v1.include_router(
    skills.router,
    prefix=Prefix.SKILLS,
    tags=[Tags.SKILLS],
)

admin_api_v1.include_router(
    medicaments.router,
    prefix=Prefix.MEDICAMENTS,
    tags=[Tags.MEDICAMENTS],
)
