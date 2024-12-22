
from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


class EmotionSaver(Protocol):
    @abstractmethod
    async def create(self, entity: EmotionDM) -> None:
        raise NotImplementedError


class EmotionReader(Protocol):
    @abstractmethod
    async def get_by_id(self, pk: EmotionId) -> EmotionDM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[OwnEmotionDTO]:
        raise NotImplementedError


# class EmotionDTOReader(Protocol):
#     @abstractmethod
#     async def get_dto_by_id(self, id: EmotionId) -> OwnEmotionDTO | None:
#         raise NotImplementedError


class EmotionUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: EmotionId) -> EmotionDM | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: EmotionDM) -> None:
        raise NotImplementedError


class EmotionDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: EmotionId) -> None:
        raise NotImplementedError
