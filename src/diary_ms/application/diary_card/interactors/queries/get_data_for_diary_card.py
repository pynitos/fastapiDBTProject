import logging

from src.diary_ms.application.common.interfaces.handlers.query import QueryHandler
from src.diary_ms.application.common.interfaces.id_provider import IdProvider
from src.diary_ms.application.diary_card.dto.data_for_diary_card import DataForDiaryCardDTO, GetDataForDiaryCardQuery
from src.diary_ms.application.diary_card.dto.diary_card import EmotionDTO
from src.diary_ms.application.diary_card.dto.mappers.emotion import EmotionDTOMapper
from src.diary_ms.application.diary_card.dto.mappers.skill import SkillDTOMapper
from src.diary_ms.application.diary_card.dto.skill import SkillDTO
from src.diary_ms.application.diary_card.interfaces.gateway import EmotionReader, SkillReader
from src.diary_ms.application.medicament.dto.mappers.medicament import MedicamentDTOMapper
from src.diary_ms.application.medicament.dto.medicament import OwnMedicamentDTO
from src.diary_ms.application.medicament.interfaces.gateway import MedicamentReader
from src.diary_ms.application.target_behavior.dto.mappers.target_behavior import TargetDTOMapper
from src.diary_ms.application.target_behavior.dto.target_behavior import OwnTargetDTO
from src.diary_ms.application.target_behavior.interfaces.gateway import TargetReader
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId

logger = logging.getLogger(__name__)


class GetDataForDiaryCard(QueryHandler[GetDataForDiaryCardQuery, DataForDiaryCardDTO]):
    def __init__(
        self,
        emotion_gateway: EmotionReader,
        skill_gateway: SkillReader,
        target_gateway: TargetReader,
        medicament_gateway: MedicamentReader,
        id_provider: IdProvider,
    ) -> None:
        self._emotion_gateway = emotion_gateway
        self._skill_gateway = skill_gateway
        self._target_gateway = target_gateway
        self._medicament_gateway = medicament_gateway
        self._id_provider = id_provider
        self._emotion_mapper = EmotionDTOMapper
        self._skill_mapper = SkillDTOMapper
        self._target_mapper = TargetDTOMapper
        self._medicament_mapper = MedicamentDTOMapper

    async def __call__(self, query: GetDataForDiaryCardQuery) -> DataForDiaryCardDTO:
        user_id: UserId = self._id_provider.get_current_user_id()
        emotions: list[Emotion] = await self._emotion_gateway.get_all(offset=0, limit=100)
        skills: list[Skill] = await self._skill_gateway.get_all(type=query.skill_type, offset=0, limit=100)
        targets: list[Target] = await self._target_gateway.get_all(user_id=user_id, offset=0, limit=100)
        meds: list[Medicament] = await self._medicament_gateway.get_all(user_id=user_id, offset=0, limit=100)
        emotions_dtos: list[EmotionDTO] = self._emotion_mapper.dm_list_to_dto_list(emotions)
        skills_dtos: list[SkillDTO] = self._skill_mapper.dm_list_to_dto_list(skills)
        targets_dtos: list[OwnTargetDTO] = self._target_mapper.dm_list_to_dto_list(targets)
        meds_dtos: list[OwnMedicamentDTO] = self._medicament_mapper.dm_list_to_dto_list(meds)
        dto = DataForDiaryCardDTO(emotions_dtos, skills_dtos, targets_dtos, meds_dtos)
        return dto
