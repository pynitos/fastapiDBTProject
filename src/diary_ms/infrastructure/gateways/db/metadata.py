from src.diary_ms.infrastructure.gateways.db.base import Base  # noqa


from src.diary_ms.infrastructure.gateways.models.diary_card import *  # noqa
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion  # noqa
from src.diary_ms.infrastructure.gateways.models.medicament import Medicament  # noqa
from src.diary_ms.infrastructure.gateways.models.skill import Skill  # noqa
from src.diary_ms.infrastructure.gateways.models.target import Target  # noqa

metadata = Base.metadata
