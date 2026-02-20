from collections.abc import AsyncIterable
from datetime import timedelta

from dishka import AnyOf, Provider, Scope, WithParents, decorate, from_context, provide, provide_all
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from taskiq import AsyncBroker, ScheduleSource

from src.diary_ms.application.common.dispatcher import DishkaResolver, DispatcherImpl, RegistryImpl
from src.diary_ms.application.common.interfaces.dispatcher.base import Registry
from src.diary_ms.application.common.interfaces.dispatcher.resolver import Resolver
from src.diary_ms.application.common.interfaces.file_manager import FileManager
from src.diary_ms.application.common.interfaces.task_sender import TaskSender
from src.diary_ms.application.common.interfaces.uow import TransactionManager
from src.diary_ms.application.diary_card.dto.commands.create_diary_card import CreateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.commands.delete_diary_card import (
    DeleteDiaryCardCommand,
)
from src.diary_ms.application.diary_card.dto.commands.update_diary_card import UpdateDiaryCardCommand
from src.diary_ms.application.diary_card.dto.data_for_diary_card import GetDataForDiaryCardQuery
from src.diary_ms.application.diary_card.dto.diary_card import GetOwnDiaryCardQuery, GetOwnDiaryCardsQuery
from src.diary_ms.application.diary_card.dto.mappers.diary_card import DiaryCardDTOMapperImpl
from src.diary_ms.application.diary_card.interactors.commands.create_diary_card import (
    CreateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.create_diary_cards_report import (
    CreateDiaryCardsReport,
    CreateDiaryCardsReportCommand,
)
from src.diary_ms.application.diary_card.interactors.commands.create_diary_cards_report_task import (
    CreateDiaryCardsReportTaskCommand,
    CreateDiaryCardsReportTaskHandler,
)
from src.diary_ms.application.diary_card.interactors.commands.delete_diary_card import (
    DeleteDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.commands.update_diary_card import (
    UpdateDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.events.diary_card_created import (
    DiaryCardCreatedEventHandler,
)
from src.diary_ms.application.diary_card.interactors.queries.get_data_for_diary_card import GetDataForDiaryCard
from src.diary_ms.application.diary_card.interactors.queries.get_diary_cards_report_task import (
    GetDiaryCardsReportTaskHandler,
    GetDiaryCardsReportTaskQuery,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_card import (
    GetOwnDiaryCard,
)
from src.diary_ms.application.diary_card.interactors.queries.get_own_diary_cards import (
    GetOwnDiaryCards,
)
from src.diary_ms.application.diary_card.interfaces.gateway import (
    DiaryCardDeleter,
    DiaryCardReader,
    DiaryCardSaver,
    DiaryCardUpdater,
    EmotionReader,
    SkillReader,
)
from src.diary_ms.application.diary_card.interfaces.report_generator import ReportGenerator
from src.diary_ms.application.medicament.dto.commands.create_medicament import (
    CreateMedicamentCommand,
)
from src.diary_ms.application.medicament.dto.commands.delete_medicament import (
    DeleteMedicamentCommand,
)
from src.diary_ms.application.medicament.dto.commands.update_medicament import (
    UpdateMedicamentCommand,
)
from src.diary_ms.application.medicament.dto.mappers.medicament import MedicamentDTOMapper
from src.diary_ms.application.medicament.dto.medicament import GetOwnMedicamentDTO, GetOwnMedicamentsDTO
from src.diary_ms.application.medicament.interactors.commands.create_medicament import CreateMedicament
from src.diary_ms.application.medicament.interactors.commands.delete_medicament import DeleteMedicament
from src.diary_ms.application.medicament.interactors.commands.update_medicament import UpdateMedicament
from src.diary_ms.application.medicament.interactors.queries.get_own_medicament_by_id import GetOwnMedicament
from src.diary_ms.application.medicament.interactors.queries.get_own_medicaments import GetOwnMedicaments
from src.diary_ms.application.medicament.interfaces.gateway import (
    MedicamentDeleter,
    MedicamentReader,
    MedicamentSaver,
    MedicamentUpdater,
)
from src.diary_ms.application.target_behavior.dto.commands.create_target import (
    CreateTargetCommand,
)
from src.diary_ms.application.target_behavior.dto.commands.delete_target import (
    DeleteTargetCommand,
)
from src.diary_ms.application.target_behavior.dto.commands.update_target import (
    UpdateTargetCommand,
)
from src.diary_ms.application.target_behavior.dto.target_behavior import (
    GetOwnAndDefaultTargetsQuery,
    GetOwnTargetQuery,
    GetOwnTargetsQuery,
)
from src.diary_ms.application.target_behavior.interactors.commands.create_target import CreateTarget
from src.diary_ms.application.target_behavior.interactors.commands.delete_target import DeleteTarget
from src.diary_ms.application.target_behavior.interactors.commands.update_target import UpdateTarget
from src.diary_ms.application.target_behavior.interactors.queries.get_own_and_default_targets import (
    GetOwnAndDefaultTargets,
)
from src.diary_ms.application.target_behavior.interactors.queries.get_own_target_by_id import GetOwnTarget
from src.diary_ms.application.target_behavior.interactors.queries.get_own_targets import GetOwnTargets
from src.diary_ms.application.target_behavior.interfaces.gateway import (
    TargetDeleter,
    TargetReader,
    TargetSaver,
    TargetUpdater,
)
from src.diary_ms.domain.model.aggregates.diary_card import DiaryCard
from src.diary_ms.domain.model.entities.emotion import Emotion
from src.diary_ms.domain.model.events.diary_card_deleted import DiaryCardCreatedEvent
from src.diary_ms.infrastructure.auth.token import JwtTokenProcessor
from src.diary_ms.infrastructure.brokers.broker import BrokerImpl
from src.diary_ms.infrastructure.brokers.interface import Broker
from src.diary_ms.infrastructure.gateways.sqla.db.session import new_session_maker
from src.diary_ms.infrastructure.gateways.sqla.diary_card import DiaryCardGateway
from src.diary_ms.infrastructure.gateways.sqla.emotion import EmotionGateway
from src.diary_ms.infrastructure.gateways.sqla.medicament import MedicamentGateway
from src.diary_ms.infrastructure.gateways.sqla.skill import SkillGateway
from src.diary_ms.infrastructure.gateways.sqla.target_behavior import TargetGateway
from src.diary_ms.infrastructure.s3.config import S3Config
from src.diary_ms.infrastructure.s3.file_manager import S3FileManager
from src.diary_ms.infrastructure.services.report_generators.pdf_report_generator import PDFReportGenerator
from src.diary_ms.infrastructure.tasks.brokers.dispatcher import TaskDispatcher
from src.diary_ms.main.config import WebConfig


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
