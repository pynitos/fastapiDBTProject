from pydantic import BaseModel


class CreateEmotionAdminReq(BaseModel):
    name: str
    description: str | None = None


class UpdateEmotionAdminReq(BaseModel):
    name: str | None = None
    description: str | None = None
