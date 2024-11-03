from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.entities import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
