from collections.abc import Callable
from typing import TypeVar


class Interactor[InputDTO, OutputDTO]:
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
InteractorFactory = Callable[[], InteractorT]
