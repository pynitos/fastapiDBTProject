from abc import ABC
from dataclasses import dataclass, field

from src.diary_ms.domain.common.model.entities.base import BaseEntity
from src.diary_ms.domain.common.model.events.base import BaseEvent


@dataclass
class AggregateRoot(BaseEntity, ABC):
    _events: list[BaseEvent] = field(
        default_factory=list, init=False, repr=False, hash=False, compare=False
    )

    def record_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def get_events(self) -> list[BaseEvent]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> list[BaseEvent]:
        events = self.get_events().copy()
        self.clear_events()
        return events
