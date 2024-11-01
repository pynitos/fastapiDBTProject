import uuid

from app.diary_ms.domain.models.id import UserId
from sqlmodel import SQLModel, Field


class User(SQLModel):
    id: UserId = Field(default_factory=uuid.uuid4, primary_key=True)
