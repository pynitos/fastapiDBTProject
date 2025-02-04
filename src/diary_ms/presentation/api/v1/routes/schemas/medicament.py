from dataclasses import dataclass


@dataclass
class CreateOwnMedicamentReq:
    name: str
    dosage: str


@dataclass
class UpdateOwnMedicamentReq:
    name: str | None = None
    dosage: str | None = None
