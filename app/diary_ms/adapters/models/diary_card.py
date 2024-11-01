from uuid import UUID

from app.diary_ms.adapters.models.base import Base


class DiaryCard(Base, table=True):
    user_id: UUID
    description: str
