import abc
from typing import Generic, TypeVar

from diary_ms.application.common.dto.request import Request

QRes = TypeVar("QRes")


class Query(Request[QRes], abc.ABC, Generic[QRes]):
    pass
