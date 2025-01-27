from uuid import uuid4

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    func,
)

from src.diary_ms.domain.model.value_objects.skill.type import SkillType

metadata = MetaData()

diary_card_skill_assotiation = Table(
    "diary_card_skill",
    metadata,
    Column("diary_card_id", metadata, ForeignKey("diary_cards.id"), primary_key=True),
    Column("skill_id", metadata, ForeignKey("skills.id"), primary_key=True),
    Column("situation", String(100), default=None, nullable=True),
)

# class DiaryCardSkill(Base):
# skill: Mapped["Skill"] = relationship(lazy="selectin")


diary_card_target_assotiation = Table(
    "diary_card_target",
    metadata,
    Column("diary_card_id", metadata, ForeignKey("diary_cards.id"), primary_key=True),
    Column("target_id", metadata, ForeignKey("targets.id"), primary_key=True),
)

diary_card_emotion_assotiation = Table(
    "diary_card_emotion",
    metadata,
    Column("diary_card_id", metadata, ForeignKey("diary_cards.id"), primary_key=True),
    Column("emotion_id", metadata, ForeignKey("emotions.id"), primary_key=True),
)

diary_card_medicament_assotiation = Table(
    "diary_card_medicament",
    metadata,
    Column("diary_card_id", metadata, ForeignKey("diary_cards.id"), primary_key=True),
    Column("medicament_id", metadata, ForeignKey("medicaments.id"), primary_key=True),
)

diary_cards_table = Table(
    "diary_cards",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("created_at", TIMESTAMP, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Column("user_id", UUID(as_uuid=True)),
    Column("mood", Integer),
    Column("description", String(1000)),
    Column("date_of_entry", TIMESTAMP(timezone=False), server_default=func.now()),
    Column(
        "type",
        Enum(SkillType, name="skill_type", create_type=False),
        nullable=False,
        default=SkillType.DBT,
    ),
)

emotions_table = Table(
    "emotions",
    metadata,
    Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True),
    Column("created_at", TIMESTAMP, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Column("name", String(20)),
    Column("description", String(100)),
)

targets_table = Table(
    "targets",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("created_at", TIMESTAMP, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Column("user_id", UUID(as_uuid=True)),
    Column("urge", String(50)),
    Column("action", String(200)),
)

skills_table = Table(
    "skills",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("created_at", TIMESTAMP, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Column("category", String(20)),
    Column("group", String(20)),
    Column("name", String(20)),
    Column("description", String(200)),
    Column(
        "type",
        Enum(SkillType, name="skill_type", create_type=False),
        nullable=False,
        default=SkillType.DBT,
    ),
)

medicaments_table = Table(
    "medicaments",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("created_at", TIMESTAMP, server_default=func.now()),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Column("user_id", UUID(as_uuid=True)),
    Column("name", String(20)),
    Column("dosage", String(20)),
)
