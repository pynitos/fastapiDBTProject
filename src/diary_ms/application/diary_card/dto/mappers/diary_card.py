from src.diary_ms.application.diary_card.dto.diary_card import (
    EmotionDTO,
    MedicamentDTO,
    OwnDiaryCardDTO,
    SkillDTO,
    TargetDTO,
)
from src.diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament


class DiaryCardDTOMapperImpl(DiaryCardDTOMapper):
    @classmethod
    def dm_to_dto(cls, dm: DiaryCard) -> OwnDiaryCardDTO:
        """
        Converts DiaryCard domain model to DTO with validation
        Args:
            dm: DiaryCard - diary card domain model
        Returns:
            OwnDiaryCardDTO: DTO for presentation
        Raises:
            AppError: If required fields are missing
        """
        if not dm.id.value:
            raise AppError("Diary Card Id Not Provided!")

        try:
            # Validate required fields
            required_fields = [dm.user_id.value, dm.mood.value, dm.date_of_entry.value, dm.type]
            if None in required_fields:
                raise AppError("Required fields are missing in DiaryCard")

            return OwnDiaryCardDTO(
                id=dm.id.value,
                user_id=dm.user_id.value,
                mood=dm.mood.value,
                description=dm.description.value if dm.description else None,
                date_of_entry=dm.date_of_entry.value,
                type=dm.type,
                targets=cls._map_targets(dm),
                emotions=cls._map_emotions(dm.emotions) if dm.emotions else None,
                medicaments=cls._map_medicaments(dm.medicaments) if dm.medicaments else None,
                skills=cls._map_skills(dm) if dm.skills and dm.skill_usages else None,
            )

        except (ValueError, AttributeError) as e:
            raise AppError(f"Mapping error: {str(e)}") from e

    @classmethod
    def _map_targets(cls, dm: DiaryCard) -> list[TargetDTO] | None:
        """Maps target behaviors with coping strategies"""
        if not dm.targets or not dm.coping_strategies:
            return None

        target_map = {t.id.value: t for t in dm.targets if t.id.value}
        return [
            TargetDTO(
                id=target.id.value,
                user_id=target.user_id.value,
                urge=target.urge.value,
                action=next(
                    (
                        cs.action.value
                        for cs in dm.coping_strategies
                        if cs.target_id.value == target.id.value and cs.action
                    ),
                    None,
                ),
                effectiveness=next(
                    (
                        cs.effectiveness.value
                        for cs in dm.coping_strategies
                        if cs.target_id.value == target.id.value and cs.effectiveness
                    ),
                    None,
                ),
            )
            for target in dm.targets
            if target.id.value and target.id.value in target_map
        ]

    @classmethod
    def _map_emotions(cls, emotions: list[Emotion]) -> list[EmotionDTO]:
        """Maps emotions"""
        return [
            EmotionDTO(
                id=e.id.value,
                name=e.name.value,
                description=e.description.value if e.description else None,
            )
            for e in emotions
            if e.id.value and e.name.value
        ]

    @classmethod
    def _map_medicaments(cls, medicaments: list[Medicament]) -> list[MedicamentDTO]:
        """Maps medications"""
        return [
            MedicamentDTO(
                id=m.id.value,
                user_id=m.user_id.value,
                name=m.name.value,
                dosage=m.dosage.value if m.dosage else None,
            )
            for m in medicaments
            if m.id.value and m.name.value
        ]

    @classmethod
    def _map_skills(cls, dm: DiaryCard) -> list[SkillDTO]:
        """Maps skills with usage situations"""
        skill_map = {s.id.value: s for s in dm.skills if s.id.value}
        return [
            SkillDTO(
                id=skill.id.value,
                category=skill.category.value,
                group=skill.group.value,
                name=skill.name.value,
                situation=next(
                    (
                        su.situation.value
                        for su in dm.skill_usages
                        if su.skill_id.value == skill.id.value and su.situation
                    ),
                    None,
                ),
            )
            for skill in dm.skills
            if skill.id.value and skill.id.value in skill_map
        ]

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[DiaryCard]) -> list[OwnDiaryCardDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
