from dishka import AsyncContainer, make_async_container
from dishka.integrations import faststream as faststream_integration
from dishka.integrations.fastapi import FastapiProvider
from faststream import FastStream
from faststream.kafka import KafkaBroker
from taskiq import AsyncBroker, ScheduleSource

from src.diary_ms.infrastructure.tasks.brokers.broker import schedule_source, task_broker
from src.diary_ms.main.config import WebConfig, web_config
from src.diary_ms.main.ioc import AdaptersProvider, InteractorsProvider
from src.diary_ms.presentation.amqp.v1.controllers.diary_cards import AMQPDiaryCardController
from src.diary_ms.presentation.api.dependencies.base_provider import AdaptersFastapiProvider

container: AsyncContainer = make_async_container(
    AdaptersProvider(),
    InteractorsProvider(),
    FastapiProvider(),
    AdaptersFastapiProvider(),
    context={WebConfig: web_config, AsyncBroker: task_broker, ScheduleSource: schedule_source},
)


async def get_faststream_app() -> FastStream:
    broker: KafkaBroker = KafkaBroker(web_config.BROKER_URI)
    faststream_app = FastStream(broker=broker)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    broker.include_router(AMQPDiaryCardController)
    return faststream_app
