import taskiq_fastapi
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.taskiq import setup_dishka
from taskiq import AsyncBroker, TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from src.diary_ms.infrastructure.tasks.brokers.registry import register_tasks
from src.diary_ms.main.config import Settings, settings
from src.diary_ms.main.ioc import AdaptersProvider, InteractorsProvider
from src.diary_ms.presentation.api.dependencies.base_provider import AdaptersFastapiProvider

result_backend: RedisAsyncResultBackend = RedisAsyncResultBackend(settings.REDIS_URI, result_ex_time=9000)  # type: ignore
task_broker: ListQueueBroker = ListQueueBroker(
    url=settings.REDIS_URI,
).with_result_backend(result_backend)

register_tasks(task_broker)

schedule_source = RedisScheduleSource(settings.REDIS_URI)
scheduler = TaskiqScheduler(task_broker, sources=[schedule_source])

container: AsyncContainer = make_async_container(
    AdaptersProvider(),
    InteractorsProvider(),
    FastapiProvider(),
    AdaptersFastapiProvider(),
    context={Settings: settings, AsyncBroker: task_broker, TaskiqScheduler: scheduler},
)
setup_dishka(container, task_broker)

taskiq_fastapi.init(task_broker, "src.diary_ms.main.web:diary_app")
