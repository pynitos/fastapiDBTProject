from sqlalchemy.engine import TupleResult
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicament import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood
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
        db_entity: DiaryCard = DiaryCard(
            user_id=entity.user_id,
            mood=entity.mood.value,
            description=entity.description.value,
            date_of_entry=entity.date_of_entry.value,
            targets=[Target(user_id=entity.user_id, urge=x.urge.value, action=x.action.value) for x in entity.targets],
            emotions=[Emotion(name=x.name.value, description=x.description.value) for x in entity.emotions],
            medicaments=[Medicament(user_id=entity.user_id, name=x.name.value, dosage=x.dosage.value) for x in entity.medicaments],
            skills=[Skill(category=x.category.value, group=x.group.value, name=x.name.value, type=x.type) for x in entity.skills],
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
                targets=[TargetDM(
                    id=x.id,
                    user_id=entity.user_id,
                    urge=TargetUrge(x.urge),
                    action=TargetAction(x.action)
                ) for x in entity.targets],
                emotions=[EmotionDM(id=x.id, name=x.name, description=x.description) for x in entity.emotions],
                medicaments=[MedicamentDM(id=x.id, user_id=entity.user_id, name=x.name, dosage=x.dosage) for x in
                             entity.medicaments],
                skills=[SkillDM(id=x.id, category=x.category, group=x.group, name=x.name, type=x.type) for x in
                        entity.skills],
            )
            domain_list.append(domain_entity)
        return domain_list
