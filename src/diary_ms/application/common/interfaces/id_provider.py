from abc import abstractmethod
from typing import Protocol

from src.diary_ms.domain.model.entities.user_id import UserId


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError


class AdminIdProvider(Protocol):
    @abstractmethod
    def get_admin_user_id(self) -> UserId:
        raise NotImplementedError
