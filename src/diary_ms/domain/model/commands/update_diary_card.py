from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class UpdateDiaryCardCommand:
    id: UUID
    mood: int | None = None
    description: str | None = None
    date_of_entry: date | None = None
    targets: list[UUID] | None = None
    emotions: list[UUID] | None = None
    medicaments: list[UUID] | None = None
    skills: list[UUID] | None = None
