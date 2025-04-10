import uuid

from sqlalchemy import select

from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.entities.skill import Skill
from src.diary_ms.domain.model.entities.target_behavior import Target
from src.diary_ms.domain.model.entities.user_id import UserId
from src.diary_ms.domain.model.value_objects.emotion.description import EmotionDescription
from src.diary_ms.domain.model.value_objects.emotion.name import EmotionName
from src.diary_ms.domain.model.value_objects.skill.category import SkillCategory
from src.diary_ms.domain.model.value_objects.skill.description import SkillDescription
from src.diary_ms.domain.model.value_objects.skill.group import SkillGroup
from src.diary_ms.domain.model.value_objects.skill.name import SkillName
from src.diary_ms.domain.model.value_objects.skill.type import SkillType
from src.diary_ms.domain.model.value_objects.target_behavior.coping_strategy.action import CopingAction
from src.diary_ms.domain.model.value_objects.target_behavior.is_default import TargetIsDefault
from src.diary_ms.domain.model.value_objects.target_behavior.urge import TargetUrge
from src.diary_ms.infrastructure.gateways.sqla.db.session import new_session_maker
from src.diary_ms.main.config import web_config

from .tables import emotions_table, skills_table, targets_table


def get_default_skills() -> list[Skill]:
    return [
        # Навыки осознанности
        Skill(
            name=SkillName("Наблюдение"),
            category=SkillCategory("Навыки осознанности 'Что?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription(
                "Навык наблюдения помогает замечать свои мысли, чувства и окружающую обстановку без оценки."
            ),
        ),
        Skill(
            name=SkillName("Описание"),
            category=SkillCategory("Навыки осознанности 'Что?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription(
                "Навык описания позволяет выражать свои переживания словами, не добавляя интерпретаций."
            ),
        ),
        Skill(
            name=SkillName("Участие"),
            category=SkillCategory("Навыки осознанности 'Как?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription(
                "Навык участия помогает полностью погружаться в текущий момент и действовать эффективно."
            ),
        ),
        Skill(
            name=SkillName("Безоценочность"),
            category=SkillCategory("Навыки осознанности 'Как?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription(
                "Навык не-суждения позволяет принимать вещи такими, какие они есть, без оценки."
            ),
        ),
        Skill(
            name=SkillName("Однонаправленность"),
            category=SkillCategory("Навыки осознанности 'Как?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription("Навык фокусировки на одной задаче или переживании в текущий момент."),
        ),
        Skill(
            name=SkillName("Эффективность"),
            category=SkillCategory("Навыки осознанности 'Как?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription(
                "Навык эффективности помогает действовать в соответствии с целями, а не эмоциями."
            ),
        ),
        Skill(
            name=SkillName("Осознанность к текущим мыслям"),
            category=SkillCategory("Навыки осознанности 'Что?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription("Навык осознания своих мыслей без вовлечения в них."),
        ),
        Skill(
            name=SkillName("Радикальное принятие"),
            category=SkillCategory("Навыки осознанности 'Как?'"),
            group=SkillGroup("Навыки осознанности"),
            type=SkillType.DBT,
            description=SkillDescription("Навык полного принятия реальности, даже если она болезненна."),
        ),
        # Навыки эмоциональной регуляции
        Skill(
            name=SkillName("Идентификация эмоций"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык распознавания и называния своих эмоций."),
        ),
        Skill(
            name=SkillName("Изменение эмоциональных реакций"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык изменения интенсивности или продолжительности эмоций."),
        ),
        Skill(
            name=SkillName("Снижение уязвимости к эмоциям"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык заботы о себе для снижения эмоциональной уязвимости."),
        ),
        Skill(
            name=SkillName("Проверка фактов"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык проверки соответствия эмоций реальным фактам."),
        ),
        Skill(
            name=SkillName("ЗАБОТА"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык заботы о себе для улучшения эмоционального состояния."),
        ),
        Skill(
            name=SkillName("Противоположное действие"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык выполнения действий, противоположных текущим эмоциям."),
        ),
        Skill(
            name=SkillName("Осознанность к текущим эмоциям"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык осознания своих эмоций без подавления или усиления."),
        ),
        Skill(
            name=SkillName("Вырабатывать мастерство"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык развития компетенций для повышения уверенности."),
        ),
        Skill(
            name=SkillName("Справляться заранее"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык подготовки к стрессовым ситуациям заранее."),
        ),
        Skill(
            name=SkillName("Аккумулирование положительных эмоций"),
            category=SkillCategory("Эмоциональная регуляция"),
            group=SkillGroup("Эмоциональная регуляция"),
            type=SkillType.DBT,
            description=SkillDescription("Навык накопления положительных эмоций для улучшения общего состояния."),
        ),
        # Навыки терпимости к дистрессу
        Skill(
            name=SkillName("Принятие реальности"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык принятия реальности, даже если она болезненна."),
        ),
        Skill(
            name=SkillName("Кризисное выживание"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык переживания кризисных ситуаций без ухудшения положения."),
        ),
        Skill(
            name=SkillName("СТОП"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык остановки перед импульсивными действиями."),
        ),
        Skill(
            name=SkillName("ТРУД"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык терпения, расслабления, успокоения и доверия."),
        ),
        Skill(
            name=SkillName("ПЕРЕЖИТЬ"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык переживания сложных эмоций без ухудшения ситуации."),
        ),
        Skill(
            name=SkillName("Улучшить момент"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык улучшения текущего момента через позитивные действия."),
        ),
        Skill(
            name=SkillName("Самоуспокоение"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык использования пяти чувств для успокоения в стрессовых ситуациях."),
        ),
        Skill(
            name=SkillName("Анализ последствий"),
            category=SkillCategory("Терпимость к дистрессу"),
            group=SkillGroup("Терпимость к дистрессу"),
            type=SkillType.DBT,
            description=SkillDescription("Навык анализа последствий действий перед их выполнением."),
        ),
        # Навыки межличностной эффективности
        Skill(
            name=SkillName("Эффективное общение"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык ясного и уважительного выражения своих потребностей."),
        ),
        Skill(
            name=SkillName("Установление границ"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык установления и поддержания здоровых границ в отношениях."),
        ),
        Skill(
            name=SkillName("Валидация"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык подтверждения чувств и переживаний другого человека."),
        ),
        Skill(
            name=SkillName("ПОПРОСИ"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык формулирования просьб и получения желаемого."),
        ),
        Skill(
            name=SkillName("Как научиться отказывать?"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык отказа в уважительной и уверенной манере."),
        ),
        Skill(
            name=SkillName("ДРУГ"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык построения и поддержания дружеских отношений."),
        ),
        Skill(
            name=SkillName("ЧЕСТЬ"),
            category=SkillCategory("Эффективность в межличностных отношениях"),
            group=SkillGroup("Эффективность в межличностных отношениях"),
            type=SkillType.DBT,
            description=SkillDescription("Навык уважения себя и других в межличностных отношениях."),
        ),
    ]


def get_default_emotions() -> list[Emotion]:
    return [
        Emotion(
            name=EmotionName("Счастье"),
            description=EmotionDescription("Чувство удовольствия и радости, связанное с положительными событиями."),
        ),
        Emotion(
            name=EmotionName("Грусть"),
            description=EmotionDescription("Чувство печали или уныния, часто вызванное потерей или разочарованием."),
        ),
        Emotion(
            name=EmotionName("Злость"),
            description=EmotionDescription(
                "Сильное чувство недовольства или раздражения, часто направленное на кого-то или что-то."
            ),
        ),
        Emotion(
            name=EmotionName("Страх"),
            description=EmotionDescription(
                "Чувство тревоги или беспокойства, вызванное возможной угрозой или опасностью."
            ),
        ),
        Emotion(
            name=EmotionName("Отвращение"),
            description=EmotionDescription("Чувство неприязни или отторжения, вызванное чем-то неприятным."),
        ),
        Emotion(
            name=EmotionName("Любовь"),
            description=EmotionDescription("Глубокое чувство привязанности и заботы к кому-то или чему-то."),
        ),
        Emotion(
            name=EmotionName("Вина"),
            description=EmotionDescription("Чувство ответственности за неправильный поступок или ошибку."),
        ),
        Emotion(
            name=EmotionName("Стыд"),
            description=EmotionDescription("Чувство неловкости или унижения из-за своих действий или качеств."),
        ),
        Emotion(
            name=EmotionName("Интерес"),
            description=EmotionDescription("Чувство вовлеченности и любопытства к чему-то новому или увлекательному."),
        ),
        Emotion(
            name=EmotionName("Спокойствие"),
            description=EmotionDescription("Чувство умиротворения и отсутствия тревоги."),
        ),
        Emotion(
            name=EmotionName("Зависть"),
            description=EmotionDescription("Чувство недовольства из-за чужого успеха или преимущества."),
        ),
        Emotion(
            name=EmotionName("Ревность"),
            description=EmotionDescription("Чувство беспокойства или страха потерять внимание или любовь кого-то."),
        ),
        Emotion(
            name=EmotionName("Благодарность"),
            description=EmotionDescription("Чувство признательности за что-то хорошее, что произошло."),
        ),
        Emotion(
            name=EmotionName("Одиночество"),
            description=EmotionDescription("Чувство изоляции или отсутствия связи с другими."),
        ),
    ]


def get_default_targets() -> list[Target]:
    # Фейковый UUID администратора
    ADMIN_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
    targets = [
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Кризисное суицидальное поведение"),
            action=CopingAction("Использовать навыки стрессоустойчивости, обратиться за помощью."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Селфхарм"),
            action=CopingAction("Использовать навыки стрессоустойчивости: ПЕРЕЖИТЬ, СТОП, ТРУД."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Суицидальные мысли"),
            action=CopingAction("Использовать навык проверки фактов для анализа мыслей."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Препятствующее терапии поведение"),
            action=CopingAction("Использовать навыки эмоциональной регуляции"),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Поведение, ухудшающее качество жизни"),
            action=CopingAction("Применить навыки решения проблем"),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Алгоколизм или наркомания"),
            action=CopingAction("Использовать навыки диалектического отказа."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Опасные половые связи"),
            action=CopingAction("Использовать навыки стрессоустойчивости и межличностной эффективности."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Эмоциональное переедание"),
            action=CopingAction("Применить навык осознанности к текущим эмоциям и выбрать альтернативное действие."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Избегание социальных ситуаций"),
            action=CopingAction("Применить навык противоположного действия для участия в социальных событиях."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Чрезмерная самокритика"),
            action=CopingAction("Использовать навык самоуспокоения и радикального принятия."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Прокрастинация"),
            action=CopingAction("Разбить задачу на мелкие шаги и использовать навык участия."),
            is_default=TargetIsDefault(True),
        ),
        Target(
            user_id=UserId(ADMIN_USER_ID),
            urge=TargetUrge("Конфликты в отношениях"),
            action=CopingAction("Применить навык DEAR MAN для эффективного общения."),
            is_default=TargetIsDefault(True),
        ),
    ]
    return targets


async def init_db() -> None:
    session_maker = new_session_maker(web_config)

    skills: list[Skill] = get_default_skills()
    emotions: list[Emotion] = get_default_emotions()
    targets: list[Target] = get_default_targets()

    async with session_maker() as session:
        for skill in skills:
            existing_skill = await session.execute(select(Skill).where(skills_table.c.name == skill.name.value))
            if not existing_skill.scalar():
                session.add(skill)

        for emotion in emotions:
            existing_emotion = await session.execute(select(Emotion).where(emotions_table.c.name == emotion.name.value))
            if not existing_emotion.scalar():
                session.add(emotion)

        for target in targets:
            existing_target = await session.execute(
                select(Target).where(
                    (targets_table.c.urge == target.urge.value) & (targets_table.c.action == target.action.value)
                )
            )
            if not existing_target.scalar():
                session.add(target)

        await session.commit()
