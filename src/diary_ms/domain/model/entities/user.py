import uuid

from src.diary_ms.domain.model.entities.id import UserId
from sqlmodel import SQLModel, Field


class User(SQLModel):
    id: UserId = Field(default_factory=uuid.uuid4, primary_key=True)
