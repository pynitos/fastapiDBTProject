import abc
from typing import Generic, TypeVar

CRes = TypeVar("CRes")


class Command(abc.ABC, Generic[CRes]):
    pass
