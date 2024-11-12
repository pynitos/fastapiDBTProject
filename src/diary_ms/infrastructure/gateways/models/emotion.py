from src.diary_ms.infrastructure.gateways.models.base import Base


class Emotion(Base, table=True):
    name: str
    description: str = None
