from dataclasses import dataclass

from diary_ms.domain.model.entities.user_id import UserId


@dataclass
class User:
    id: UserId
