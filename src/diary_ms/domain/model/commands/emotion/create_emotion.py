from dataclasses import dataclass


@dataclass
class CreateEmotionAdminCommand:
    name: str
    description: str | None = None
