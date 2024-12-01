from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.diary_ms.domain.model.entities.user_id import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UUID:
        raise NotImplementedError
