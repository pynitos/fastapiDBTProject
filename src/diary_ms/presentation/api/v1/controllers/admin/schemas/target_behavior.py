from dataclasses import dataclass


@dataclass
class CreateTargetAdminReq:
    urge: str
    action: str


@dataclass
class UpdateTargetAdminReq:
    urge: str | None = None
    action: str | None = None
