import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from taskiq import AsyncBroker, ScheduleSource

from src.diary_ms.infrastructure.log.main import configure_logging
from src.diary_ms.infrastructure.tasks.brokers.broker import schedule_source, task_broker
from src.diary_ms.presentation.telegram.common.provider import TgProvider
from src.diary_ms.presentation.telegram.controllers.diary_cards.create_diary_card import create_diary_card_dialog
from src.diary_ms.presentation.telegram.controllers.diary_cards.get_diary_cards import own_diary_cards_dialog
from src.diary_ms.presentation.telegram.controllers.main_menu import main_menu_dialog
from src.diary_ms.presentation.telegram.controllers.medicaments import medicament_router
from src.diary_ms.presentation.telegram.controllers.start import start_router

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


def get_dispatcher(_: BotConfig) -> Dispatcher:
    dp = Dispatcher()
    # dp.update.middleware(IdProviderMiddleware())
    dp.include_router(start_router)
    dp.include_router(main_menu_dialog)
    dp.include_router(create_diary_card_dialog)
    dp.include_router(own_diary_cards_dialog)
    dp.include_router(medicament_router)
    setup_dishka(container=container, router=dp, auto_inject=True)
    setup_dialogs(dp)
    logger.info("DP done.")
    return dp


async def bot_main():
    logger.info("start")
    bot = Bot(config.bot_token)
    await get_dispatcher(config).start_polling(bot)
