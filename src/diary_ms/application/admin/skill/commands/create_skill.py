from uuid import uuid4

from src.diary_ms.application.admin.skill.interfaces.gateway import SkillAdminSaver
from src.diary_ms.application.common.interfaces.handlers.command import CommandHandler
from src.diary_ms.application.common.interfaces.id_provider import AdminIdProvider
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.skill.create_skill_admin import CreateSkillAdminCommand
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName


class CreateSkillAdminHandler(CommandHandler[CreateSkillAdminCommand, None]):
    def __init__(
        self,
        db_gateway: SkillAdminSaver,
        id_provider: AdminIdProvider,
        transaction_manager: TransactionManager,
    ) -> None:
        self.db_gateway = db_gateway
        self.id_provider = id_provider
        self.transaction_manager = transaction_manager

    async def __call__(self, command: CreateSkillAdminCommand) -> None:
        self.id_provider.get_admin_user_id()
        skill: Skill = Skill.create(
            id=SkillId(uuid4()),
            name=SkillName(command.name),
            category=SkillCategory(command.category) if command.category else None,
            group=SkillGroup(command.group),
            description=SkillDescription(command.description) if command.description else None,
            skill_type=command.type,
        )
        await self.db_gateway.create(skill)
        await self.transaction_manager.commit()
