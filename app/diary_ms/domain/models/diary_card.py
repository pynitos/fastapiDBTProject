import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from uuid import UUID

from app.diary_ms.domain.models.base import BaseDM


@dataclass
class DiaryCardDM(BaseDM):
    user_id: UUID
    description: str
