from src.diary_ms.infrastructure.gateways.models.base import Base


class Skill(Base, table=True):
    category: str
    group: str
    name: str
    type: str = 'dbt'
