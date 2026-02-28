from sqlalchemy.orm import composite, registry, relationship

from diary_ms.domain.model.aggregates.diary_card import DiaryCard
from diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId
from diary_ms.domain.model.entities.coping_strategy import CopingStrategy
from diary_ms.domain.model.entities.emotion import Emotion
from diary_ms.domain.model.entities.medicament import Medicament
from diary_ms.domain.model.entities.skill import Skill
from diary_ms.domain.model.entities.skill_application import SkillApplication
from diary_ms.domain.model.entities.target_behavior import Target
from diary_ms.domain.model.entities.user_id import UserId
from diary_ms.domain.model.value_objects.diary_card.date_of_entry import DCDateOfEntry
from diary_ms.domain.model.value_objects.diary_card.description import DCDescription
from diary_ms.domain.model.value_objects.diary_card.mood import DCMood
from diary_ms.domain.model.value_objects.emotion.description import EmotionDescription
from diary_ms.domain.model.value_objects.emotion.id import EmotionId
from diary_ms.domain.model.value_objects.emotion.name import EmotionName
from diary_ms.domain.model.value_objects.medicament.id import MedicamentId
from diary_ms.domain.model.value_objects.skill.category import SkillCategory
from diary_ms.domain.model.value_objects.skill.description import SkillDescription
from diary_ms.domain.model.value_objects.skill.effectiveness import SkillEffectiveness
from diary_ms.domain.model.value_objects.skill.group import SkillGroup
from diary_ms.domain.model.value_objects.skill.id import SkillId
from diary_ms.domain.model.value_objects.skill.name import SkillName
from diary_ms.domain.model.value_objects.skill.situation import SkillUsage
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.id import CopingStrategyId
from diary_ms.domain.model.value_objects.target_behavior.coping_strategy.intensity import UrgeIntensity
from diary_ms.domain.model.value_objects.target_behavior.id import TargetId
from diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge
from diary_ms.infrastructure.gateways.sqla.db.tables import (
    diary_card_skill_assotiation,
    diary_card_target_assotiation,
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
            "targets": relationship("Target", secondary="diary_card_target", lazy="selectin", viewonly=True),
            "coping_strategies": relationship("CopingStrategy", lazy="selectin"),
            "medicaments": relationship("Medicament", secondary="diary_card_medicament", lazy="selectin"),
            "skills": relationship("Skill", secondary="diary_card_skill", lazy="selectin", viewonly=True),
            "skill_usages": relationship("SkillApplication", lazy="selectin"),
        },
    )

    mapper_registry.map_imperatively(
        SkillApplication,
        diary_card_skill_assotiation,
        properties={
            "diary_card_id": composite(lambda value: DiaryCardId(value), diary_card_skill_assotiation.c.diary_card_id),
            "__diary_card_id": diary_card_skill_assotiation.c.diary_card_id,
            "skill_id": composite(lambda value: SkillId(value), diary_card_skill_assotiation.c.skill_id),
            "__skill_id": diary_card_skill_assotiation.c.skill_id,
            "usage": composite(lambda value: SkillUsage(value), diary_card_skill_assotiation.c.usage),
            "__usage": diary_card_skill_assotiation.c.usage,
            "effectiveness": composite(
                lambda value: SkillEffectiveness(value) if value is not None else None,
                diary_card_skill_assotiation.c.effectiveness,
            ),
            "__effectiveness": diary_card_skill_assotiation.c.effectiveness,
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
            "diary_card_assotiations": relationship("SkillApplication", cascade="all, delete-orphan", lazy="selectin"),
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
            "action": composite(lambda value: CopingAction(value), targets_table.c.action),
            "__action": targets_table.c.action,
            "is_default": composite(lambda value: TargetIsDefault(value), targets_table.c.is_default),
            "__is_default": targets_table.c.is_default,
        },
    )
    mapper_registry.map_imperatively(
        CopingStrategy,
        diary_card_target_assotiation,
        properties={
            "id": composite(lambda value: CopingStrategyId(value), diary_card_target_assotiation.c.id),
            "__id": diary_card_target_assotiation.c.id,  # Сырое значение для SQL
            "target_id": composite(lambda value: TargetId(value), diary_card_target_assotiation.c.target_id),
            "__target_id": diary_card_target_assotiation.c.target_id,
            "action": composite(lambda value: CopingAction(value), diary_card_target_assotiation.c.action),
            "__action": diary_card_target_assotiation.c.action,
            "urge_intensity": composite(
                lambda value: UrgeIntensity(value) if value else None,
                diary_card_target_assotiation.c.effectiveness,
            ),
            "__urge_intensity": diary_card_target_assotiation.c.urge_intensity,
            "effectiveness": composite(
                lambda value: SkillEffectiveness(value) if value else None,
                diary_card_target_assotiation.c.effectiveness,
            ),
            "__effectiveness": diary_card_target_assotiation.c.effectiveness,
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
            "dosage": composite(lambda value: CopingAction(value), medicaments_table.c.dosage),
            "__dosage": medicaments_table.c.dosage,
        },
    )
