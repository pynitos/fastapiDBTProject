from abc import abstractmethod
from typing import Any, Protocol


class TaskSender(Protocol):
    @abstractmethod
    def send_task(self, message: Any, topic: str, schedule: list[Any]) -> None:
        raise NotImplementedError
