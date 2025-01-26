import logging

from src.diary_ms.application.admin.skill.dto.mapper.skill import SkillAdminDTOMapper
from src.diary_ms.application.admin.skill.dto.skill import GetSkillsAdminDTO, SkillAdminDTO
from src.diary_ms.application.admin.skill.interfaces.gateway import SkillAdminReader
from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.domain.model.entities.skill import Skill

logger = logging.getLogger(__name__)


class GetSkillsAdminHandler(QueryHandler[GetSkillsAdminDTO, list[SkillAdminDTO]]):
    def __init__(self, db_gateway: SkillAdminReader, id_provider: AdminIdProvider, mapper: SkillAdminDTOMapper):
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self._mapper = mapper

    async def __call__(self, query: GetSkillsAdminDTO) -> list[SkillAdminDTO]:
        self._id_provider.get_admin_user_id()
        skills: list[Skill] = await self._db_gateway.get_all(
            offset=query.pagination.offset, limit=query.pagination.limit
        )
        logger.debug(f"Get Skills Use case: {skills}")
        dtos = self._mapper.dm_list_to_dto_list(skills)
        return dtos
