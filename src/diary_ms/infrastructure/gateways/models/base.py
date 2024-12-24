from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.diary_ms.infrastructure.gateways.db.base import Base


class BaseMixin(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
