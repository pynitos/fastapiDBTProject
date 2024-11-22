import logging

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from src.diary_ms.main.config import Settings, settings
from src.diary_ms.main.ioc import AdaptersProvider, InteractorProvider
from src.diary_ms.presentation.api.v1.api import api_v1


def create_fastapi_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.include_router(api_v1)
    app = VersionedFastAPI(
        app,
        version_format="{major}",
        prefix_format="/api/v{major}",
    )
    return app


def create_app():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )
    app = create_fastapi_app()
    container = make_async_container(
        AdaptersProvider(),
        InteractorProvider(),
        FastapiProvider(),
        context={Settings: settings},
    )
    setup_dishka(container, app)
    return app


diary_app: FastAPI = create_app()
