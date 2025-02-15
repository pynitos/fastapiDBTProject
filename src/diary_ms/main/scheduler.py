import asyncio

from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler

from .web import container


async def get_scheduler():
    task_broker = await container.get(BrokerWrapper)
    scheduler: StreamScheduler = StreamScheduler(
        broker=task_broker,
        sources=[LabelScheduleSource(task_broker)],
    )
    return scheduler


if "__name__" == "__main__":
    asyncio.run(get_scheduler())
