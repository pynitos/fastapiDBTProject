from uuid import UUID

from sqlalchemy.engine import TupleResult
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.diary_ms.application.common.exceptions.diary_card import DiaryCardNotFoundError
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicament import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import (
    DCDateOfEntry,
)
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName
from src.diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from src.diary_ms.domain.model.value_objects.medicament.name import MedicamentName
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.domain.model.value_objects.target_behavior.action import TargetAction
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge
from src.diary_ms.infrastructure.gateways.base import BaseGateway
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion
from src.diary_ms.infrastructure.gateways.models.medicament import Medicament
from src.diary_ms.infrastructure.gateways.models.skill import Skill
from src.diary_ms.infrastructure.gateways.models.target import Target


class DiaryCardGateway(BaseGateway[DiaryCard, DiaryCardDM]):
    def create(self, entity: DiaryCardDM) -> None:
        targets: list[Target] = None
        emotions: list[Emotion] = None
        medicaments: list[Medicament] = None
        skills: list[Skill] = None
        db_entity: DiaryCard = DiaryCard(
            user_id=entity.user_id,
            mood=entity.mood.value,
            description=entity.description.value,
            date_of_entry=entity.date_of_entry.value,
            targets=targets,
            emotions=emotions,
            medicaments=medicaments,
            skills=skills,
        )
        self._session.add(db_entity)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[DiaryCardDM]:
        stmt: SelectOfScalar = select(self._db_model).offset(offset).limit(limit)
        result: TupleResult = await self._session.exec(stmt)
        result_list: list[DiaryCard] = result.all()
        domain_list: list[DiaryCardDM] = []
        for entity in result_list:
            domain_entity: DiaryCardDM = DiaryCardDM(
                id=entity.id,
                user_id=entity.user_id,
                mood=DCMood(entity.mood),
                description=DCDescription(entity.description),
                date_of_entry=DCDateOfEntry(entity.date_of_entry),
                targets=[
                    TargetDM(
                        id=x.id,
                        user_id=entity.user_id,
                        urge=TargetUrge(x.urge),
                        action=TargetAction(x.action),
                    )
                    for x in entity.targets
                ],
                emotions=[
                    EmotionDM(
                        id=x.id,
                        name=EmotionName(x.name),
                        description=EmotionDescription(x.description),
                    )
                    for x in entity.emotions
                ],
                medicaments=[
                    MedicamentDM(
                        id=x.id,
                        user_id=entity.user_id,
                        name=MedicamentName(x.name),
                        dosage=MedicamentDosage(x.dosage),
                    )
                    for x in entity.medicaments
                ],
                skills=[
                    SkillDM(
                        id=x.id,
                        category=SkillCategory(x.category),
                        group=SkillGroup(x.group),
                        name=SkillName(x.name),
                        type=SkillType(x.type),
                    )
                    for x in entity.skills
                ],
            )
            domain_list.append(domain_entity)
        return domain_list

    async def _get_by_id(self, pk: UUID) -> DiaryCard | None:
        return await self._session.get(self._db_model, pk)

    async def get_by_id(self, pk: UUID) -> DiaryCardDM | None:
        entity: DiaryCard | None = await self._get_by_id(pk=pk)
        if not entity:
            return None
        return DiaryCardDM(
            id=entity.id,
            user_id=entity.user_id,
            mood=DCMood(entity.mood),
            description=DCDescription(entity.description),
            date_of_entry=DCDateOfEntry(entity.date_of_entry),
            targets=[
                TargetDM(
                    id=x.id,
                    user_id=entity.user_id,
                    urge=TargetUrge(x.urge),
                    action=TargetAction(x.action),
                )
                for x in entity.targets
            ],
            emotions=[
                EmotionDM(
                    id=x.id,
                    name=EmotionName(x.name),
                    description=EmotionDescription(x.description),
                )
                for x in entity.emotions
            ],
            medicaments=[
                MedicamentDM(
                    id=x.id,
                    user_id=entity.user_id,
                    name=MedicamentName(x.name),
                    dosage=MedicamentDosage(x.dosage),
                )
                for x in entity.medicaments
            ],
            skills=[
                SkillDM(
                    id=x.id,
                    category=SkillCategory(x.category),
                    group=SkillGroup(x.group),
                    name=SkillName(x.name),
                    type=SkillType(x.type),
                )
                for x in entity.skills
            ],
        )

    async def update(self, entity: DiaryCardDM) -> None:
        pk = entity.id
        db_entity: DiaryCard = await self._get_by_id(pk)
        if not db_entity:
            raise DiaryCardNotFoundError

        if entity.mood:
            db_entity.mood = entity.mood.value
        if entity.description:
            db_entity.description = entity.description.value
        if entity.date_of_entry:
            db_entity.date_of_entry = entity.date_of_entry.value
        if entity.targets:
            db_entity.targets = [
                Target(user_id=entity.user_id, urge=x.urge.value, action=x.action.value)
                for x in entity.targets
            ]
        if entity.emotions:
            db_entity.emotions = [
                Emotion(name=x.name.value, description=x.description.value)
                for x in entity.emotions
            ]
        if entity.medicaments:
            db_entity.medicaments = [
                Medicament(
                    user_id=entity.user_id, name=x.name.value, dosage=x.dosage.value
                )
                for x in entity.medicaments
            ]
        if entity.skills:
            db_entity.skills = [
                Skill(
                    category=x.category.value,
                    group=x.group.value,
                    name=x.name.value,
                    type=x.type,
                )
                for x in entity.skills
            ]

        self._session.add(db_entity)

    async def delete(self, pk: DiaryCardId) -> None:
        entity: DiaryCard | None = await self._session.get(self._db_model, pk)
        if not entity:
            raise DiaryCardNotFoundError
        await self._session.delete(entity)
