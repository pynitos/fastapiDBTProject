import taskiq_fastapi
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.taskiq import setup_dishka, inject, FromDishka
from taskiq import AsyncBroker, TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from src.diary_ms.application.common.dto.pagination import Pagination
from src.diary_ms.application.common.interfaces.dispatcher.base import Sender
from src.diary_ms.application.diary_card.dto.diary_card import GetOwnDiaryCardsDTO, OwnDiaryCardDTO
from src.diary_ms.main.config import Settings, settings
from src.diary_ms.main.ioc import AdaptersProvider, InteractorsProvider
from src.diary_ms.presentation.api.dependencies.base_provider import AdaptersFastapiProvider

result_backend: RedisAsyncResultBackend = RedisAsyncResultBackend(settings.REDIS_URI, result_ex_time=9000)  # type: ignore
task_broker: ListQueueBroker = ListQueueBroker(
    url=settings.REDIS_URI,
).with_result_backend(result_backend)
redis_source = RedisScheduleSource(settings.REDIS_URI)
scheduler = TaskiqScheduler(task_broker, sources=[redis_source])


@task_broker.task
@inject
async def create_diary_cards_report_(sender: FromDishka[Sender]):
    result = await sender.send_query(
        GetOwnDiaryCardsDTO(Pagination(limit=10, offset=0))
        )
    return result


container: AsyncContainer = make_async_container(
    AdaptersProvider(),
    InteractorsProvider(),
    FastapiProvider(),
    AdaptersFastapiProvider(),
    context={Settings: settings, AsyncBroker: task_broker, TaskiqScheduler: scheduler},
)
setup_dishka(container, task_broker)

taskiq_fastapi.init(task_broker, "src.diary_ms.main.web:diary_app")
