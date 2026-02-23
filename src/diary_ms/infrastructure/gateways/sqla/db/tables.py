from uuid import uuid4

from sqlalchemy import (
    DATE,
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    SmallInteger,
    String,
    Table,
    func,
)

from src.diary_ms.domain.model.value_objects.skill.type import SkillType

metadata = MetaData()

diary_card_skill_assotiation = Table(
    "diary_card_skill",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("diary_card_id", UUID(as_uuid=True), ForeignKey("diary_cards.id", ondelete="CASCADE")),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE")),
    Column("usage", String(200), default=None, nullable=True),
    Column("effectiveness", SmallInteger, default=None, nullable=True),
)

diary_card_target_assotiation = Table(
    "diary_card_target",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("diary_card_id", UUID(as_uuid=True), ForeignKey("diary_cards.id", ondelete="CASCADE")),
    Column("target_id", UUID(as_uuid=True), ForeignKey("targets.id", ondelete="CASCADE")),
    Column("action", String(500), default=None, nullable=True),
    Column("urge_intensity", SmallInteger, default=None, nullable=True),
    Column("effectiveness", SmallInteger, default=None, nullable=True),
)

diary_card_emotion_assotiation = Table(
    "diary_card_emotion",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("diary_card_id", UUID(as_uuid=True), ForeignKey("diary_cards.id", ondelete="CASCADE")),
    Column("emotion_id", UUID(as_uuid=True), ForeignKey("emotions.id", ondelete="CASCADE")),
)

diary_card_medicament_assotiation = Table(
    "diary_card_medicament",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("diary_card_id", UUID(as_uuid=True), ForeignKey("diary_cards.id", ondelete="CASCADE")),
    Column("medicament_id", UUID(as_uuid=True), ForeignKey("medicaments.id", ondelete="CASCADE")),
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
    Column("date_of_entry", DATE, server_default=func.now()),
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
    Column("name", String(100)),
    Column("description", String(200)),
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
    Column("urge", String(100)),
    Column("action", String(500), default=None, nullable=True),
    Column("is_default", Boolean, default=False),
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
    Column("category", String(100)),
    Column("group", String(100)),
    Column("name", String(100)),
    Column("description", String(300)),
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
    Column("dosage", String(100)),
)
