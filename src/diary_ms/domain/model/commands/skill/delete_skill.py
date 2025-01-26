from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteSkillAdminCommand:
    id: UUID
