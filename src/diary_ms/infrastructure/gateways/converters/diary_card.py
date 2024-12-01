from collections.abc import Sequence

from pydantic import NonNegativeInt

from src.diary_ms.application.dto.diary_card import (
    EmotionDTO,
    MedicamentDTO,
    OwnDiaryCardDTO,
    SkillDTO,
    TargetDTO,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCardDM
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.emotion import EmotionDM
from src.diary_ms.domain.model.entities.medicament import MedicamentDM
from src.diary_ms.domain.model.entities.skill import SkillDM
from src.diary_ms.domain.model.entities.target_behavior import TargetDM
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import (
    DCDateOfEntry,
)
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from src.diary_ms.domain.model.value_objects.emotion.description import (
    EmotionDescription,
)
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName
from src.diary_ms.domain.model.value_objects.medicament.dosage import MedicamentDosage
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from src.diary_ms.domain.model.value_objects.medicament.name import MedicamentName
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.domain.model.value_objects.target_behavior.action import TargetAction
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge
from src.diary_ms.infrastructure.gateways.models.diary_card import DiaryCard


class DiaryCardMapper:
    @classmethod
    def db_list_to_dto_list(cls, db_list: Sequence[DiaryCard]) -> list[OwnDiaryCardDTO]:
        dto_list: list[OwnDiaryCardDTO] = []
        for entity in db_list:
            dto_entity: OwnDiaryCardDTO = cls.db_to_dto(entity)
            dto_list.append(dto_entity)
        return dto_list

    @classmethod
    def db_to_dto(cls, entity: DiaryCard) -> OwnDiaryCardDTO:
        return OwnDiaryCardDTO(
            id=entity.id,
            user_id=entity.user_id,
            mood=entity.mood,
            description=entity.description,
            date_of_entry=entity.date_of_entry,
            type=SkillType(entity.type),
            targets=[
                TargetDTO(
                    urge=x.urge,
                    action=x.action,
                )
                for x in entity.targets
            ]
            if entity.targets and isinstance(entity.targets, list)
            else None,
            emotions=[
                EmotionDTO(
                    name=x.name,
                    description=x.description,
                )
                for x in entity.emotions
            ] if isinstance(entity.emotions, list) else None,
            medicaments=[
                MedicamentDTO(
                    name=x.name,
                    dosage=x.dosage,
                )
                for x in entity.medicaments
            ] if isinstance(entity.medicaments, list) else None,
            skills=[
                SkillDTO(
                    category=x.category,
                    group=x.group,
                    name=x.name,
                )
                for x in entity.skills
            ]  if isinstance(entity.skills, list) else None,
        )

    @classmethod
    def db_to_dm(cls, entity: DiaryCard) -> DiaryCardDM:
        domain_entity: DiaryCardDM = DiaryCardDM(
            id=DiaryCardId(entity.id),
            user_id=UserId(entity.user_id),
            mood=DCMood(entity.mood),
            description=DCDescription(entity.description),
            date_of_entry=DCDateOfEntry(entity.date_of_entry),
            type=SkillType(entity.type),
            targets=[
                TargetDM(
                    id=TargetId(x.id),
                    user_id=UserId(entity.user_id),
                    urge=TargetUrge(x.urge),
                    action=TargetAction(x.action),
                )
                for x in entity.targets
            ]
            if entity.targets
            else None,
            emotions=[
                EmotionDM(
                    id=EmotionId(x.id),
                    name=EmotionName(x.name),
                    description=EmotionDescription(x.description),
                )
                for x in entity.emotions
            ]
            if entity.emotions
            else None,
            medicaments=[
                MedicamentDM(
                    id=MedicamentId(x.id),
                    user_id=UserId(entity.user_id),
                    name=MedicamentName(x.name),
                    dosage=MedicamentDosage(x.dosage),
                )
                for x in entity.medicaments
            ]
            if entity.medicaments
            else None,
            skills=[
                SkillDM(
                    id=SkillId(x.id),
                    category=SkillCategory(x.category),
                    group=SkillGroup(x.group),
                    name=SkillName(x.name),
                    type=SkillType(x.type),
                )
                for x in entity.skills
            ]
            if entity.skills
            else None,
        )
        return domain_entity
