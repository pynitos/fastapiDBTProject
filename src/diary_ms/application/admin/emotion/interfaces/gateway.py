from abc import abstractmethod
from typing import Protocol

from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId


class EmotionAdminSaver(Protocol):
    @abstractmethod
    async def create(self, entity: Emotion) -> None:
        raise NotImplementedError


class EmotionAdminReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: EmotionId) -> Emotion | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[EmotionAdminDTO]:
        raise NotImplementedError


# class EmotionDTOReader(Protocol):
#     @abstractmethod
#     async def get_dto_by_id(self, id: EmotionId) -> OwnEmotionDTO | None:
#         raise NotImplementedError


class EmotionAdminUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: EmotionId) -> Emotion | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Emotion) -> None:
        raise NotImplementedError


class EmotionAdminDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: EmotionId) -> None:
        raise NotImplementedError
