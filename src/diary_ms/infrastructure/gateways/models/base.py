import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, text
from sqlmodel import SQLModel, Field


class Base(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default=None,
        sa_type=TIMESTAMP(),
        sa_column_kwargs={
            "nullable": False,
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )
    updated_at: datetime = Field(
        default=None,
        sa_type=TIMESTAMP(),
        sa_column_kwargs={
            "nullable": False,
            "server_default": text("CURRENT_TIMESTAMP"),
            "server_onupdate": text("CURRENT_TIMESTAMP"),
        },
    )