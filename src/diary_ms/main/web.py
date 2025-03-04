import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations import faststream as faststream_integration
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from faststream import FastStream
from faststream.kafka import KafkaBroker
from taskiq import AsyncBroker, ScheduleSource

from src.diary_ms.infrastructure.tasks.brokers.broker import schedule_source, scheduler, task_broker
from src.diary_ms.main.config import WebConfig, web_config
from src.diary_ms.main.ioc import AdaptersProvider, InteractorsProvider
from src.diary_ms.presentation.amqp.v1.controllers.diary_cards import AMQPDiaryCardController
from src.diary_ms.presentation.api import v1
from src.diary_ms.presentation.api.dependencies.base_provider import (
    AdaptersFastapiProvider,
)
from src.diary_ms.presentation.api.exceptions import include_exception_handlers

logger: logging.Logger = logging.getLogger(__name__)

container: AsyncContainer = make_async_container(
    AdaptersProvider(),
    InteractorsProvider(),
    FastapiProvider(),
    AdaptersFastapiProvider(),
    context={WebConfig: web_config, AsyncBroker: task_broker, ScheduleSource: schedule_source},
)


async def get_faststream_app() -> FastStream:
    broker: KafkaBroker = await container.get(KafkaBroker)
    faststream_app = FastStream(broker=broker)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    broker.include_router(AMQPDiaryCardController)
    return faststream_app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    logger.info("Start app lifespan.")
    await get_faststream_app()
    if not task_broker.is_worker_process:
        await task_broker.startup()
        await scheduler.startup()
    logger.debug("Scheduler started.")
    yield
    if not task_broker.is_worker_process:
        await task_broker.shutdown()
        await scheduler.shutdown()
    await app.state.dishka_container.close()
    logger.debug("Close app lifespan.")


def create_fastapi_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=web_config.PROJECT_NAME,
        docs_url=f"{web_config.API_PREFIX}/docs",
        redoc_url=f"{web_config.API_PREFIX}/redoc",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    include_exception_handlers(app)
    app.mount(f"{web_config.API_PREFIX}/v1", v1.api)

    @app.get(f"{web_config.API_PREFIX}/v1/openapi.json", name="1.0", tags=["Versions"])
    @app.get(f"{web_config.API_PREFIX}/v1/docs", name="1.0", tags=["Documentations"])
    @app.get(
        f"{web_config.API_PREFIX}/v1/admin/openapi.json",
        name="Admin 1.0",
        tags=["Versions"],
    )
    @app.get(
        f"{web_config.API_PREFIX}/v1/admin/docs",
        name="Admin 1.0",
        tags=["Documentations"],
    )
    def noop() -> None: ...

    return app


def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
        handlers=[logging.StreamHandler()],
    )
    app: FastAPI = create_fastapi_app()
    setup_dishka(container, app)
    logger.debug(web_config.REDIS_URI)
    return app


diary_app: FastAPI = create_app()
