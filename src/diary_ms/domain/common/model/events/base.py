from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from uuid import UUID, uuid4


@dataclass(frozen=True)
class BaseEvent(ABC):  # noqa: B024
    event_title: ClassVar[str] = ""

    event_id: UUID = field(init=False, kw_only=True, default_factory=uuid4)
    event_timestamp: datetime = field(
        init=False, kw_only=True, default_factory=datetime.now
    )
