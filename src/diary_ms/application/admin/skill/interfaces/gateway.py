from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.value_objects.skill.id import SkillId


class SkillAdminSaver(Protocol):
    @abstractmethod
    async def create(self, entity: Skill) -> None:
        raise NotImplementedError


class SkillAdminReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: SkillId) -> Skill | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Skill]:
        raise NotImplementedError


class SkillAdminUpdater(Protocol):
    @abstractmethod
    async def get_by_id(self, id: SkillId) -> Skill | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Skill) -> None:
        raise NotImplementedError


class SkillAdminDeleter(Protocol):
    @abstractmethod
    async def delete(self, id: SkillId) -> None:
        raise NotImplementedError
