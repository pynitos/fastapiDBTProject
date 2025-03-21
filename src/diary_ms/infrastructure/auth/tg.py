import uuid
from uuid import UUID

from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider, IdProvider
from src.diary_ms.domain.model.entities.user_id import UserId


class TgIdProvider(IdProvider, AdminIdProvider):
    def __init__(
        self,
        tg_user_id: int,
    ) -> None:
        self.tg_user_id = tg_user_id

    def get_current_user_id(self) -> UserId:
        id: UUID = self.tg_id_to_uuid()
        return UserId(id)

    def get_admin_user_id(self) -> UserId:
        raise NotImplementedError

    def tg_id_to_uuid(self) -> UUID:
        return uuid.uuid5(uuid.NAMESPACE_OID, str(self.tg_user_id))
