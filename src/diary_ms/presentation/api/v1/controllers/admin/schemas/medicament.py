from dataclasses import dataclass


@dataclass
class CreateMedicamentAdminReq:
    name: str
    dosage: str


@dataclass
class UpdateMedicamentAdminReq:
    name: str | None = None
    dosage: str | None = None
