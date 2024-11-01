from abc import abstractmethod
from typing import Protocol

from app.diary_ms.domain.models.id import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
