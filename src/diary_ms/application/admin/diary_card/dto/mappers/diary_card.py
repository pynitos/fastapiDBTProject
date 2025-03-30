from src.diary_ms.application.admin.diary_card.dto.diary_card import (
    DiaryCardAdminDTO,
    EmotionAdminDTO,
    MedicamentAdminDTO,
    SkillAdminDTO,
    TargetAdminDTO,
)
from src.diary_ms.domain.common.exceptions.base import AppError
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard


class DiaryCardAdminDTOMapper:
    @staticmethod
    def dm_to_dto(dm: DiaryCard) -> DiaryCardAdminDTO:
        if not dm.id.value:
            raise AppError("Diary Card Id Not Provided!")
        return DiaryCardAdminDTO(
            id=dm.id.value,
            user_id=dm.user_id.value,
            mood=dm.mood.value,
            description=dm.description.value,
            date_of_entry=dm.date_of_entry.value,
            type=dm.type,
            targets=[
                TargetAdminDTO(
                    id=x.id.value,
                    user_id=x.user_id.value,
                    urge=x.urge.value,
                    action=x.action.value,
                )
                for x in dm.coping_strategies
                if x.id.value
            ]
            if dm.coping_strategies
            else None,
            emotions=[
                EmotionAdminDTO(
                    x.id.value,
                    x.name.value,
                    x.description.value,
                )
                for x in dm.emotions
                if x.id.value
            ]
            if dm.emotions
            else None,
            medicaments=[
                MedicamentAdminDTO(
                    id=x.id.value,
                    user_id=x.user_id.value,
                    name=x.name.value,
                    dosage=x.dosage.value,
                )
                for x in dm.medicaments
                if x.id.value
            ]
            if dm.medicaments
            else None,
            skills=[
                SkillAdminDTO(
                    category=x.category.value,
                    group=x.group.value,
                    name=x.name.value,
                    situation=x.situation.value,
                )
                for x in dm.skills
            ]
            if dm.skills
            else None,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[DiaryCard]) -> list[DiaryCardAdminDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
