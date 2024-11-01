from typing import Callable, TypeVar


class BaseInteractor[InputDTO, OutputDTO]:
    def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
InteractorFactory = Callable[[], InteractorT]
