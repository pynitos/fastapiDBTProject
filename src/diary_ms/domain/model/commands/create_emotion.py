from dataclasses import dataclass


@dataclass
class CreateEmotionCommand:
    name: str
    description: str | None = None
