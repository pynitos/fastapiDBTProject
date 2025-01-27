from src.diary_ms.application.diary_card.dto.diary_card import (
    EmotionDTO,
    MedicamentDTO,
    OwnDiaryCardDTO,
    SkillDTO,
    TargetDTO,
)
from src.diary_ms.application.diary_card.interfaces.mapper import DiaryCardDTOMapper
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard


class DiaryCardDTOMapperImpl(DiaryCardDTOMapper):
    @staticmethod
    def dm_to_dto(dm: DiaryCard) -> OwnDiaryCardDTO:
        return OwnDiaryCardDTO(
            id=dm.id.value,
            user_id=dm.id.value,
            mood=dm.mood.value,
            description=dm.description.value,
            date_of_entry=dm.date_of_entry.value,
            type=dm.type.value,
            targets=[
                TargetDTO(
                    id=x.id.value,
                    user_id=x.user_id.value,
                    urge=x.urge.value,
                    action=x.action.value,
                )
                for x in dm.targets
            ]
            if dm.targets
            else None,
            emotions=[
                EmotionDTO(
                    x.id.value,
                    x.name.value,
                    x.description.value,
                )
                for x in dm.emotions
            ]
            if dm.emotions
            else None,
            medicaments=[
                MedicamentDTO(
                    id=x.id.value,
                    user_id=x.user_id.value,
                    name=x.name.value,
                    dosage=x.dosage.value,
                )
                for x in dm.medicaments
            ]
            if dm.medicaments
            else None,
            skills=[
                SkillDTO(
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
    def dm_list_to_dto_list(cls, dm_list: list[DiaryCard]) -> list[OwnDiaryCardDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
