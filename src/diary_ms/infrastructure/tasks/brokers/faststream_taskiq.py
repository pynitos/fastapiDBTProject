from typing import Any

from taskiq_faststream import BrokerWrapper


class FaststreamTaskiqTaskSenderImpl:
    def __init__(self, task_broker: BrokerWrapper):
        self.task_broker = task_broker

    def send_task(self, message: Any, topic: str, schedule: list[Any]) -> None:
        self.task_broker.task(
            message=message,
            topic=topic,
            schedule=schedule,
        )
