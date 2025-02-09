import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.diary_ms.main.config import Settings, settings
from src.diary_ms.main.ioc import AdaptersProvider, InteractorProvider
from src.diary_ms.presentation.api import v1
from src.diary_ms.presentation.api.dependencies.base_provider import (
    AdaptersFastapiProvider,
)
from src.diary_ms.presentation.api.exceptions import include_exception_handlers

logger: logging.Logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    logger.debug("Start app lifespan.")
    yield
    app.state.dishka_container.close()
    logger.debug("Close app lifespan.")


def create_fastapi_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    include_exception_handlers(app)
    app.mount(f"{settings.API_PREFIX}/v1", v1.api)

    @app.get(f"{settings.API_PREFIX}/v1/openapi.json", name="1.0", tags=["Versions"])
    @app.get(f"{settings.API_PREFIX}/v1/docs", name="1.0", tags=["Documentations"])
    @app.get(
        f"{settings.API_PREFIX}/v1/admin/openapi.json",
        name="Admin 1.0",
        tags=["Versions"],
    )
    @app.get(
        f"{settings.API_PREFIX}/v1/admin/docs",
        name="Admin 1.0",
        tags=["Documentations"],
    )
    def noop() -> None: ...

    return app


def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )
    app: FastAPI = create_fastapi_app()
    container: AsyncContainer = make_async_container(
        AdaptersProvider(),
        InteractorProvider(),
        FastapiProvider(),
        AdaptersFastapiProvider(),
        context={Settings: settings},
    )
    setup_dishka(container, app)
    return app


diary_app: FastAPI = create_app()
