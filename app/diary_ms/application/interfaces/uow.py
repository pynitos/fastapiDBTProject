from abc import abstractmethod
from typing import Protocol


class UOWProtocol(Protocol):
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
