from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler
from taskiq_redis import RedisAsyncResultBackend

from src.diary_ms.infrastructure.brokers.message_broker import message_broker
from src.diary_ms.main.config import settings

result_backend: RedisAsyncResultBackend = RedisAsyncResultBackend(settings.REDIS_URI)  # type: ignore
task_broker: BrokerWrapper = BrokerWrapper(message_broker).with_result_backend(result_backend)

diary_cards_get_report_task = task_broker.task(
    "task message", topic="get_diary_cards", schedule=[{"cron": "*/1 * * * *"}]
)

scheduler: StreamScheduler = StreamScheduler(
    broker=task_broker,
    sources=[LabelScheduleSource(task_broker)],
)
