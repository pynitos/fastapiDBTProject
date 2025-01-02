from collections.abc import Sequence

from src.diary_ms.application.admin.emotion.dto.emotion import EmotionAdminDTO
from src.diary_ms.infrastructure.gateways.models.emotion import Emotion


class EmotionMapper:
    @classmethod
    def db_list_to_dto_list(cls, db_list: Sequence[Emotion]) -> list[EmotionAdminDTO]:
        dto_list: list[EmotionAdminDTO] = []
        for entity in db_list:
            dto_entity: EmotionAdminDTO = cls.db_to_dto(entity)
            dto_list.append(dto_entity)
        return dto_list

    @classmethod
    def db_to_dto(cls, entity: Emotion) -> EmotionAdminDTO:
        return EmotionAdminDTO(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            description=entity.description,
        )

    # @classmethod
    # def db_to_dm(cls, entity: DiaryCard) -> DiaryCardDM:
    #     domain_entity: DiaryCardDM = DiaryCardDM(
    #         id=DiaryCardId(entity.id),
    #         user_id=UserId(entity.user_id),
    #         mood=DCMood(entity.mood),
    #         description=DCDescription(entity.description),
    #         date_of_entry=DCDateOfEntry(entity.date_of_entry),
    #         type=SkillType(entity.type),
    #         targets=[
    #             TargetDM(
    #                 id=TargetId(x.id),
    #                 user_id=UserId(entity.user_id),
    #                 urge=TargetUrge(x.urge),
    #                 action=TargetAction(x.action),
    #             )
    #             for x in entity.targets
    #         ]
    #         if entity.targets
    #         else None,
    #         emotions=[
    #             EmotionDM(
    #                 id=EmotionId(x.id),
    #                 name=EmotionName(x.name),
    #                 description=EmotionDescription(x.description),
    #             )
    #             for x in entity.emotions
    #         ]
    #         if entity.emotions
    #         else None,
    #         medicaments=[
    #             MedicamentDM(
    #                 id=MedicamentId(x.id),
    #                 user_id=UserId(entity.user_id),
    #                 name=MedicamentName(x.name),
    #                 dosage=MedicamentDosage(x.dosage),
    #             )
    #             for x in entity.medicaments
    #         ]
    #         if entity.medicaments
    #         else None,
    #         skills=[
    #             SkillDM(
    #                 id=SkillId(x.id),
    #                 category=SkillCategory(x.category),
    #                 group=SkillGroup(x.group),
    #                 name=SkillName(x.name),
    #                 type=SkillType(x.type),
    #             )
    #             for x in entity.skills
    #         ]
    #         if entity.skills
    #         else None,
    #     )
    #     return domain_entity
