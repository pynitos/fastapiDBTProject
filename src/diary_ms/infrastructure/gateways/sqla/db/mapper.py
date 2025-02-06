from sqlalchemy.orm import composite, registry, relationship

from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from src.diary_ms.domain.model.entities.diary_card_skill import DiaryCardSkillAssotiation
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from src.diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from src.diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from src.diary_ms.domain.model.value_objects.emotion.description import EmotionDescription
from src.diary_ms.domain.model.value_objects.emotion.id import EmotionId
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName
from src.diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.id import SkillId
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.situation import SkillSituation
from src.diary_ms.domain.model.value_objects.target_behavior.action import TargetAction
from src.diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge
from src.diary_ms.infrastructure.gateways.sqla.db.tables import (
    diary_card_skill_assotiation,
    diary_cards_table,
    emotions_table,
    medicaments_table,
    metadata,
    skills_table,
    targets_table,
)

mapper_registry = registry(metadata=metadata)


def init_mapper() -> None:
    mapper_registry.map_imperatively(
        DiaryCard,
        diary_cards_table,
        properties={
            "id": composite(lambda value: DiaryCardId(value), diary_cards_table.c.id),
            "__id": diary_cards_table.c.id,
            "user_id": composite(lambda value: UserId(value), diary_cards_table.c.user_id),
            "__user_id": diary_cards_table.c.user_id,
            "mood": composite(lambda value: DCMood(value), diary_cards_table.c.mood),
            "__mood": diary_cards_table.c.mood,
            "description": composite(lambda value: DCDescription(value), diary_cards_table.c.description),
            "__description": diary_cards_table.c.description,
            "date_of_entry": composite(lambda value: DCDateOfEntry(value), diary_cards_table.c.date_of_entry),
            "__date_of_entry": diary_cards_table.c.date_of_entry,
            "emotions": relationship("Emotion", secondary="diary_card_emotion", lazy="selectin"),
            "medicaments": relationship("Medicament", secondary="diary_card_medicament", lazy="selectin"),
            "skills": relationship("Skill", secondary="diary_card_skill", lazy="selectin", viewonly=True),
            "skill_assotiations": relationship("DiaryCardSkillAssotiation", lazy="selectin"),
        },
    )

    mapper_registry.map_imperatively(
        DiaryCardSkillAssotiation,
        diary_card_skill_assotiation,
        properties={
            "diary_card_id": composite(lambda value: DiaryCardId(value), diary_card_skill_assotiation.c.diary_card_id),
            "__diary_card_id": diary_card_skill_assotiation.c.diary_card_id,
            "skill_id": composite(lambda value: SkillId(value), diary_card_skill_assotiation.c.skill_id),
            "__skill_id": diary_card_skill_assotiation.c.skill_id,
            "situation": composite(lambda value: SkillSituation(value), diary_card_skill_assotiation.c.situation),
            "__situation": diary_card_skill_assotiation.c.situation,
        },
    )

    mapper_registry.map_imperatively(
        Skill,
        skills_table,
        properties={
            "id": composite(lambda value: SkillId(value), skills_table.c.id),
            "__id": skills_table.c.id,
            "category": composite(lambda value: SkillCategory(value), skills_table.c.category),
            "__category": skills_table.c.category,
            "group": composite(lambda value: SkillGroup(value), skills_table.c.group),
            "__group": skills_table.c.group,
            "name": composite(lambda value: SkillName(value), skills_table.c.name),
            "__name": skills_table.c.name,
            "description": composite(lambda value: SkillDescription(value), skills_table.c.description),
            "__description": skills_table.c.description,
            "diary_card_assotiations": relationship(
                "DiaryCardSkillAssotiation", cascade="all, delete-orphan", lazy="selectin"
            ),
        },
    )
    mapper_registry.map_imperatively(
        Emotion,
        emotions_table,
        properties={
            "id": composite(lambda value: EmotionId(value), emotions_table.c.id),
            "__id": emotions_table.c.id,
            "name": composite(lambda value: EmotionName(value), emotions_table.c.name),
            "__name": emotions_table.c.name,
            "description": composite(lambda value: EmotionDescription(value), emotions_table.c.description),
            "__description": emotions_table.c.description,
        },
    )
    mapper_registry.map_imperatively(
        Target,
        targets_table,
        properties={
            "id": composite(lambda value: TargetId(value), targets_table.c.id),
            "__id": targets_table.c.id,
            "user_id": composite(lambda value: UserId(value), targets_table.c.user_id),
            "__user_id": targets_table.c.user_id,
            "urge": composite(lambda value: TargetUrge(value), targets_table.c.urge),
            "__urge": targets_table.c.urge,
            "action": composite(lambda value: TargetAction(value), targets_table.c.action),
            "__action": targets_table.c.action,
            "is_default": composite(lambda value: TargetIsDefault(value), targets_table.c.action),
            "__is_default": targets_table.c.action,
        },
    )
    mapper_registry.map_imperatively(
        Medicament,
        medicaments_table,
        properties={
            "id": composite(lambda value: MedicamentId(value), medicaments_table.c.id),
            "__id": medicaments_table.c.id,
            "user_id": composite(lambda value: UserId(value), medicaments_table.c.user_id),
            "__user_id": medicaments_table.c.user_id,
            "name": composite(lambda value: TargetUrge(value), medicaments_table.c.name),
            "__name": medicaments_table.c.name,
            "dosage": composite(lambda value: TargetAction(value), medicaments_table.c.dosage),
            "__dosage": medicaments_table.c.dosage,
        },
    )
