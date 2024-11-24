from dataclasses import dataclass, field
from datetime import date
from uuid import UUID


@dataclass
class CreateDiaryCardCommand:
    mood: int

    id: UUID | None = None
    user_id: UUID = None
    description: str | None = None
    date_of_entry: date = field(default_factory=date.today)

    targets: list[UUID] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[UUID] | None = None
