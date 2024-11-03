import uuid
from datetime import datetime, UTC

from sqlmodel import SQLModel, Field


class Base(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
