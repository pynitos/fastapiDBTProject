from src.diary_ms.application.admin.diary_card.dto.diary_card import (
    DiaryCardAdminDTO,
    EmotionAdminDTO,
    MedicamentAdminDTO,
    SkillAdminDTO,
    TargetAdminDTO,
)
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.medicament import Medicament
from src.diary_ms.domain.model.entities.skill import Skill


class DiaryCardAdminDTOMapper:
    @classmethod
    def dm_to_dto(cls, dm: DiaryCard) -> DiaryCardAdminDTO:
        """
        Converts DiaryCard domain model to Admin DTO with validation
        Args:
            dm: DiaryCard - diary card domain model
        Returns:
            DiaryCardAdminDTO: DTO for admin presentation
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

            return DiaryCardAdminDTO(
                id=dm.id.value,
                user_id=dm.user_id.value,
                mood=dm.mood.value,
                description=dm.description.value if dm.description else None,
                date_of_entry=dm.date_of_entry.value,
                type=dm.type,
                targets=cls._map_targets(dm),
                emotions=cls._map_emotions(dm.emotions) if dm.emotions else None,
                medicaments=cls._map_medicaments(dm.medicaments) if dm.medicaments else None,
                skills=cls._map_skills(dm.skills) if dm.skills else None,
            )

        except (ValueError, AttributeError) as e:
            raise AppError(f"Mapping error: {str(e)}") from e

    @classmethod
    def _map_targets(cls, dm: DiaryCard) -> list[TargetAdminDTO] | None:
        """Maps target behaviors with coping strategies for admin view"""
        if not dm.targets or not dm.coping_strategies:
            return None

        target_map = {t.id.value: t for t in dm.targets if t.id.value}
        return [
            TargetAdminDTO(
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
                effectiveness=next(  # Добавлено поле effectiveness из примера
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
    def _map_emotions(cls, emotions: list[Emotion]) -> list[EmotionAdminDTO] | None:
        """Maps emotions for admin view"""
        if not emotions:
            return None

        return [
            EmotionAdminDTO(
                id=e.id.value,
                name=e.name.value,
                description=e.description.value if e.description else None,
            )
            for e in emotions
            if e.id.value and e.name.value
        ]

    @classmethod
    def _map_medicaments(cls, medicaments: list[Medicament]) -> list[MedicamentAdminDTO] | None:
        """Maps medications for admin view"""
        if not medicaments:
            return None

        return [
            MedicamentAdminDTO(
                id=m.id.value,
                user_id=m.user_id.value,
                name=m.name.value,
                dosage=m.dosage.value,
            )
            for m in medicaments
            if m.id.value and m.name.value
        ]

    @classmethod
    def _map_skills(cls, skills: list[Skill]) -> list[SkillAdminDTO] | None:
        """Maps skills for admin view"""
        if not skills:
            return None

        return [
            SkillAdminDTO(
                category=s.category.value if s.category else None,
                group=s.group.value if s.group else None,
                name=s.name.value,
                situation=s.situation.value if s.situation else None,
            )
            for s in skills
            if s.name.value
        ]

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[DiaryCard]) -> list[DiaryCardAdminDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
