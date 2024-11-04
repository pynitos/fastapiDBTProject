from uuid import UUID

from src.diary_ms.adapters.models.base import Base


class DiaryCard(Base, table=True):
    user_id: UUID
    description: str
