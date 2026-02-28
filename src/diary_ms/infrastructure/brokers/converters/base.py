from dataclasses import asdict
from typing import Any

import orjson

from diary_ms.domain.common.model.events.base import Event


def convert_event_to_broker_message(event: Event) -> bytes:
    return orjson.dumps(event)


def convert_event_to_json(event: Event) -> dict[str, Any]:
    return asdict(event)
