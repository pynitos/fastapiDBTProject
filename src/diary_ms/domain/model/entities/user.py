import uuid
from dataclasses import dataclass, field

from src.diary_ms.domain.model.entities.user_id import UserId


@dataclass
class User:
    id: UserId
