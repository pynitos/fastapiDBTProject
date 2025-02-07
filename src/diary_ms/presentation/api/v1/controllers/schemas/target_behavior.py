from dataclasses import dataclass


@dataclass
class CreateOwnTargetReq:
    urge: str
    action: str


@dataclass
class UpdateOwnTargetReq:
    urge: str | None = None
    action: str | None = None