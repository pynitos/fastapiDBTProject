from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from src.diary_ms.infrastructure.tasks.brokers.registry import register_tasks
from src.diary_ms.main.config import settings
from src.diary_ms.main.ioc import AdaptersProvider, InteractorsProvider

result_backend: RedisAsyncResultBackend = RedisAsyncResultBackend(settings.REDIS_URI)  # type: ignore
task_broker: ListQueueBroker = ListQueueBroker(
    url=settings.REDIS_URI,
    result_backend=result_backend,
)

register_tasks(task_broker)

redis_source = RedisScheduleSource(settings.REDIS_URI)
scheduler = TaskiqScheduler(task_broker, sources=[redis_source])

container = make_async_container(AdaptersProvider(), InteractorsProvider())
setup_dishka(container, task_broker)
