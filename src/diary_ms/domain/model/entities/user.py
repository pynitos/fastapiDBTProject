import uuid

from sqlmodel import SQLModel, Field

from src.diary_ms.domain.model.entities.user_id import UserId


class User(SQLModel):
    id: UserId = Field(default_factory=uuid.uuid4, primary_key=True)
