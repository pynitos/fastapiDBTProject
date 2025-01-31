from src.diary_ms.application.admin.skill.dto.mapper.skill import SkillAdminDTOMapper
from src.diary_ms.application.admin.skill.dto.skill import GetSkillAdminDTO, SkillAdminDTO
from src.diary_ms.application.admin.skill.interfaces.gateway import SkillAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.value_objects.skill.id import SkillId


class GetSkillAdminHandler(QueryHandler[GetSkillAdminDTO, SkillAdminDTO | None]):
    def __init__(self, db_gateway: SkillAdminReader, id_provider: AdminIdProvider, mapper: SkillAdminDTOMapper):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetSkillAdminDTO) -> SkillAdminDTO | None:
        self._id_provider.get_admin_user_id()
        emotion: Skill | None = await self._db_gateway.get_by_id(SkillId(query.id))
        return self._mapper.dm_to_dto(emotion) if emotion else None
