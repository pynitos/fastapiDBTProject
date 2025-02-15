from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar, Protocol

type JsonDecodable = bool | bytes | bytearray | float | int | str | None
type SendableArray = Sequence["BaseSendableMessage"]
type SendableTable = dict[str, "BaseSendableMessage"]


class StandardDataclass(Protocol):
    """Protocol to check type is dataclass."""

    __dataclass_fields__: ClassVar[dict[str, Any]]


type BaseSendableMessage = JsonDecodable | Decimal | datetime | StandardDataclass | SendableTable | SendableArray | None
