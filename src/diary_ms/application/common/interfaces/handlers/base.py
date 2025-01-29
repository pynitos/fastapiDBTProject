from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol, TypeVar

InputDTO = TypeVar("InputDTO", contravariant=True)
OutputDTO = TypeVar("OutputDTO", covariant=True)


class Handler(Protocol[InputDTO, OutputDTO]):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
InteractorFactory = Callable[[], InteractorT]
