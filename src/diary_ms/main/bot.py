import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from taskiq import AsyncBroker, ScheduleSource

from diary_ms.infrastructure.log.main import configure_logging
from diary_ms.infrastructure.tasks.brokers.broker import schedule_source, task_broker
from diary_ms.presentation.telegram.common.provider import TgProvider
from diary_ms.presentation.telegram.controllers.diary_cards.create_diary_card import create_diary_card_dialog
from diary_ms.presentation.telegram.controllers.diary_cards.get_diary_cards import own_diary_cards_dialog
from diary_ms.presentation.telegram.controllers.error_handler import error_router
from diary_ms.presentation.telegram.controllers.main_menu import main_menu_dialog
from diary_ms.presentation.telegram.controllers.medicaments import medicaments_router
from diary_ms.presentation.telegram.controllers.start import start_router
from diary_ms.presentation.telegram.controllers.targets import targets_router

from .config import BaseConfig, BotConfig, WebConfig, load_bot_config, web_config
from .ioc import AdaptersProvider, InteractorsProvider

configure_logging(web_config.log)
logger = logging.getLogger(__name__)
config = load_bot_config()
container: AsyncContainer = make_async_container(
    AdaptersProvider(),
    InteractorsProvider(),
    TgProvider(),
    context={BaseConfig: config, WebConfig: web_config, AsyncBroker: task_broker, ScheduleSource: schedule_source},
)


def get_storage(
    bot_config: BotConfig,
) -> BaseStorage:
    if bot_config.REDIS_URI:
        logger.debug("Setup redis storage")
        return RedisStorage.from_url(
            url=bot_config.REDIS_URI,
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    logger.debug("Setup memory storage")
    return MemoryStorage()


def get_dispatcher(_: BotConfig, storage: BaseStorage) -> Dispatcher:
    dp = Dispatcher(events_isolation=SimpleEventIsolation(), storage=storage)

    setup_dishka(container=container, router=dp, auto_inject=True)
    dp.include_router(error_router)
    dp.include_router(start_router)
    dp.include_router(main_menu_dialog)
    dp.include_router(create_diary_card_dialog)
    dp.include_router(own_diary_cards_dialog)
    dp.include_router(medicaments_router)
    dp.include_router(targets_router)

    setup_dialogs(dp)
    logger.debug("DP setuped.")
    return dp


async def bot_main() -> None:
    logger.info("start")
    bot = Bot(config.bot_token)
    storage = get_storage(config)
    try:
        await get_dispatcher(config, storage).start_polling(bot)
    except TelegramNetworkError:
        logger.error("TelegramNetworkError: отсутствует соединение с сервером телеграм или с интернетом")
