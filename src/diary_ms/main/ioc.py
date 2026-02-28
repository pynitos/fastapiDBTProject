from collections.abc import AsyncIterable
from datetime import timedelta

from dishka import AnyOf, Provider, Scope, WithParents, decorate, from_context, provide, provide_all
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from taskiq import AsyncBroker, ScheduleSource

from diary_ms.application.common.dispatcher import DishkaResolver, DispatcherImpl, RegistryImpl
from diary_ms.application.common.interfaces.dispatcher.base import Registry
from diary_ms.application.common.interfaces.dispatcher.resolver import Resolver
from diary_ms.application.common.interfaces.file_manager import FileManager
from diary_ms.application.common.interfaces.task_sender import TaskSender
from diary_ms.application.common.interfaces.uow import TransactionManager
from diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from diary_ms.application.diary_card.dto.commands.delete_diary_card import (
    DeleteDiaryCardCommand,
)
from diary_ms.application.diary_card.dto.commands.update_diary_card import UpdateDiaryCardCommand
from diary_ms.application.diary_card.dto.data_for_diary_card import GetDataForDiaryCardQuery
from diary_ms.application.diary_card.dto.diary_card import GetOwnDiaryCardQuery, GetOwnDiaryCardsQuery
from diary_ms.application.diary_card.dto.mappers.diary_card import DiaryCardDTOMapperImpl
from diary_ms.application.diary_card.interactors.commands.create_diary_card import (
    CreateDiaryCard,
)
from diary_ms.application.diary_card.interactors.commands.create_diary_cards_report import (
    CreateDiaryCardsReport,
    CreateDiaryCardsReportCommand,
)
from diary_ms.application.diary_card.interactors.commands.create_diary_cards_report_task import (
    CreateDiaryCardsReportTaskCommand,
    CreateDiaryCardsReportTaskHandler,
)
from diary_ms.application.diary_card.interactors.commands.delete_diary_card import (
    DeleteDiaryCard,
)
from diary_ms.application.diary_card.interactors.commands.update_diary_card import (
    UpdateDiaryCard,
)
from diary_ms.application.diary_card.interactors.events.diary_card_created import (
    DiaryCardCreatedEventHandler,
)
from diary_ms.application.diary_card.interactors.queries.get_data_for_diary_card import GetDataForDiaryCard
from diary_ms.application.diary_card.interactors.queries.get_diary_cards_report_task import (
    GetDiaryCardsReportTaskHandler,
    GetDiaryCardsReportTaskQuery,
)
from diary_ms.application.diary_card.interactors.queries.get_own_diary_card import (
    GetOwnDiaryCard,
)
from diary_ms.application.diary_card.interactors.queries.get_own_diary_cards import (
    GetOwnDiaryCards,
)
from diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
    EmotionReader,
    SkillReader,
)
from diary_ms.application.diary_card.interfaces.report_generator import ReportGenerator
from diary_ms.application.medicament.dto.commands.create_medicament import (
    CreateMedicamentCommand,
)
from diary_ms.application.medicament.dto.commands.delete_medicament import (
    DeleteMedicamentCommand,
)
from diary_ms.application.medicament.dto.commands.update_medicament import (
    UpdateMedicamentCommand,
)
from diary_ms.application.medicament.dto.mappers.medicament import MedicamentDTOMapper
from diary_ms.application.medicament.dto.medicament import GetOwnMedicamentDTO, GetOwnMedicamentsDTO
from diary_ms.application.medicament.interactors.commands.create_medicament import CreateMedicament
from diary_ms.application.medicament.interactors.commands.delete_medicament import DeleteMedicament
from diary_ms.application.medicament.interactors.commands.update_medicament import UpdateMedicament
from diary_ms.application.medicament.interactors.queries.get_own_medicament_by_id import GetOwnMedicament
from diary_ms.application.medicament.interactors.queries.get_own_medicaments import GetOwnMedicaments
from diary_ms.application.medicament.interfaces.gateway import (
    MedicamentDeleter,
    MedicamentReader,
    MedicamentSaver,
    MedicamentUpdater,
)
from diary_ms.application.target_behavior.dto.commands.create_target import (
    CreateTargetCommand,
)
from diary_ms.application.target_behavior.dto.commands.delete_target import (
    DeleteTargetCommand,
)
from diary_ms.application.target_behavior.dto.commands.update_target import (
    UpdateTargetCommand,
)
from diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnAndDefaultTargetsQuery,
    GetOwnTargetQuery,
    GetOwnTargetsQuery,
)
from diary_ms.application.target_behavior.interactors.commands.create_target import CreateTarget
from diary_ms.application.target_behavior.interactors.commands.delete_target import DeleteTarget
from diary_ms.application.target_behavior.interactors.commands.update_target import UpdateTarget
from diary_ms.application.target_behavior.interactors.queries.get_own_and_default_targets import (
    GetOwnAndDefaultTargets,
)
from diary_ms.application.target_behavior.interactors.queries.get_own_target_by_id import GetOwnTarget
from diary_ms.application.target_behavior.interactors.queries.get_own_targets import GetOwnTargets
from diary_ms.application.target_behavior.interfaces.gateway import (
    TargetDeleter,
    TargetReader,
    TargetSaver,
    TargetUpdater,
)
from diary_ms.domain.model.aggregates.diary_card import DiaryCard
from diary_ms.domain.model.entities.emotion import Emotion
from diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from diary_ms.infrastructure.auth.token import JwtTokenProcessor
from diary_ms.infrastructure.brokers.broker import BrokerImpl
from diary_ms.infrastructure.brokers.interface import Broker
from diary_ms.infrastructure.gateways.sqla.db.session import new_session_maker
from diary_ms.infrastructure.gateways.sqla.diary_card import DiaryCardGateway
from diary_ms.infrastructure.gateways.sqla.emotion import EmotionGateway
from diary_ms.infrastructure.gateways.sqla.medicament import MedicamentGateway
from diary_ms.infrastructure.gateways.sqla.skill import SkillGateway
from diary_ms.infrastructure.gateways.sqla.target_behavior import TargetGateway
from diary_ms.infrastructure.s3.config import S3Config
from diary_ms.infrastructure.s3.file_manager import S3FileManager
from diary_ms.infrastructure.services.report_generators.pdf_report_generator import PDFReportGenerator
from diary_ms.infrastructure.tasks.brokers.dispatcher import TaskDispatcher
from diary_ms.main.config import WebConfig


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(provides=WebConfig, scope=Scope.APP)
    task_borker = from_context(provides=AsyncBroker, scope=Scope.APP)
    schedule_sourse = from_context(provides=ScheduleSource, scope=Scope.APP)

    report_generator = provide(PDFReportGenerator, provides=ReportGenerator)
    file_manager = provide(S3FileManager, provides=FileManager)

    @provide(scope=Scope.APP)
    def s3_config(self, config: WebConfig) -> S3Config:
        return config.s3

    @provide(scope=Scope.APP)
    def get_jwt_token_processor(self, config: WebConfig) -> JwtTokenProcessor:
        return JwtTokenProcessor(
            secret=config.JWT_SECRET_KEY,
            expires=timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            algorithm=config.JWT_ALGORITHM,
        )

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: WebConfig) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, TransactionManager]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_broker_client(self, config: WebConfig) -> KafkaBroker:
        return KafkaBroker(config.BROKER_URI)

    @decorate
    async def get_broker_session(self, broker_client: KafkaBroker) -> AsyncIterable[KafkaBroker]:
        async with broker_client as broker:
            yield broker

    @provide(scope=Scope.REQUEST)
    async def get_broker(self, broker_session: KafkaBroker) -> AnyOf[BrokerImpl, Broker]:
        return BrokerImpl(broker_session=broker_session)

    @provide
    def get_diary_cards_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        DiaryCardGateway,
        DiaryCardReader,
        DiaryCardSaver,
        DiaryCardUpdater,
        DiaryCardDeleter,
    ]:
        return DiaryCardGateway(db_model=DiaryCard, session=session)

    @provide
    def get_emotion_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        EmotionGateway,
        EmotionReader,
    ]:
        return EmotionGateway(db_model=Emotion, session=session)

    @provide
    def get_skill_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        SkillGateway,
        SkillReader,
    ]:
        return SkillGateway(session=session)

    @provide
    def get_medicament_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        MedicamentGateway,
        MedicamentReader,
        MedicamentSaver,
        MedicamentUpdater,
        MedicamentDeleter,
    ]:
        return MedicamentGateway(session=session)

    @provide
    def get_target_gateway(
        self, session: AsyncSession
    ) -> AnyOf[
        TargetGateway,
        TargetReader,
        TargetSaver,
        TargetUpdater,
        TargetDeleter,
    ]:
        return TargetGateway(session=session)

    @provide(scope=Scope.APP)
    async def get_task_dispather(
        self, task_broker: AsyncBroker, schedule_source: ScheduleSource
    ) -> AnyOf[TaskSender, TaskDispatcher]:
        task_dispatcher: TaskDispatcher = TaskDispatcher(task_broker, schedule_source)
        return task_dispatcher


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    mappers = provide_all(
        WithParents[DiaryCardDTOMapperImpl],  # type: ignore
        MedicamentDTOMapper,
    )

    command_handlers = provide_all(
        CreateDiaryCard,
        UpdateDiaryCard,
        DeleteDiaryCard,
        CreateDiaryCardsReport,
        CreateDiaryCardsReportTaskHandler,
        CreateMedicament,
        UpdateMedicament,
        DeleteMedicament,
        CreateTarget,
        UpdateTarget,
        DeleteTarget,
    )

    query_handlers = provide_all(
        GetOwnDiaryCards,
        GetOwnDiaryCard,
        GetDataForDiaryCard,
        GetOwnMedicament,
        GetOwnMedicaments,
        GetOwnTargets,
        GetOwnAndDefaultTargets,
        GetOwnTarget,
        GetDiaryCardsReportTaskHandler,
    )

    event_handlers = provide_all(DiaryCardCreatedEventHandler, scope=Scope.REQUEST)

    dispather = provide(WithParents[DispatcherImpl], scope=Scope.REQUEST)  # type: ignore
    resolver = provide(DishkaResolver, provides=Resolver, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def init_registry(self) -> AnyOf[Registry, RegistryImpl]:
        registry = RegistryImpl()

        # Diary cards
        registry.register_command_handler(CreateDiaryCardCommand, CreateDiaryCard)
        registry.register_command_handler(UpdateDiaryCardCommand, UpdateDiaryCard)
        registry.register_command_handler(DeleteDiaryCardCommand, DeleteDiaryCard)
        registry.register_command_handler(CreateDiaryCardsReportCommand, CreateDiaryCardsReport)
        registry.register_command_handler(CreateDiaryCardsReportTaskCommand, CreateDiaryCardsReportTaskHandler)
        registry.register_query_handler(GetOwnDiaryCardQuery, GetOwnDiaryCard)
        registry.register_query_handler(GetOwnDiaryCardsQuery, GetOwnDiaryCards)
        registry.register_query_handler(GetDataForDiaryCardQuery, GetDataForDiaryCard)
        registry.register_query_handler(GetDiaryCardsReportTaskQuery, GetDiaryCardsReportTaskHandler)
        registry.register_event_handler(DiaryCardCreatedEvent, DiaryCardCreatedEventHandler)

        # Medicaments
        registry.register_command_handler(CreateMedicamentCommand, CreateMedicament)
        registry.register_command_handler(UpdateMedicamentCommand, UpdateMedicament)
        registry.register_command_handler(DeleteMedicamentCommand, DeleteMedicament)
        registry.register_query_handler(GetOwnMedicamentDTO, GetOwnMedicament)
        registry.register_query_handler(GetOwnMedicamentsDTO, GetOwnMedicaments)

        # Targets
        registry.register_command_handler(CreateTargetCommand, CreateTarget)
        registry.register_command_handler(UpdateTargetCommand, UpdateTarget)
        registry.register_command_handler(DeleteTargetCommand, DeleteTarget)
        registry.register_query_handler(GetOwnTargetQuery, GetOwnTarget)
        registry.register_query_handler(GetOwnTargetsQuery, GetOwnTargets)
        registry.register_query_handler(GetOwnAndDefaultTargetsQuery, GetOwnAndDefaultTargets)

        return registry
