import logging

from src.diary_ms.application.admin.skill.interfaces.gateway import SkillAdminUpdater
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.skill.update_skill import UpdateSkillAdminCommand
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName

logger = logging.getLogger()


class UpdateSkillAdminHandler(CommandHandler[UpdateSkillAdminCommand, None]):
    def __init__(
        self,
        db_gateway: SkillAdminUpdater,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self._db_gateway = db_gateway
        self._id_provider = id_provider
        self.transaction_manager = transaction_manager

    async def __call__(self, command: UpdateSkillAdminCommand) -> None:
        self._id_provider.get_admin_user_id()
        skill: Skill | None = await self._db_gateway.get_by_id(SkillId(command.id))
        if skill:
            updated_skill: Skill = skill.update(
                name=SkillName(command.name) if command.name else None,
                category=SkillCategory(command.category) if command.category else None,
                group=SkillGroup(command.group) if command.group else None,
                description=SkillDescription(command.description) if command.description else None,
                skill_type=command.type,
            )
            await self._db_gateway.update(updated_skill)
            logger.debug(f"Skill with id: {command.id} updated.")
            await self.transaction_manager.commit()
