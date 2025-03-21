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


def get_dispatcher(config: BotConfig) -> Dispatcher:
    dp = Dispatcher()
    setup_dishka(container=container, router=dp, auto_inject=True)
    # dp.update.middleware(IdProviderMiddleware())
    dp.include_router(start_router)
    dp.include_router(create_diary_card_dialog)
    # dp.include_router(create_wishlist_dialog)
    # dp.include_router(own_wishlists_dialog)
    # dp.include_router(wishlist_dialog)
    setup_dialogs(dp)
    logger.info("DP done.")
    return dp


def get_dispatcher_preview() -> Dispatcher:
    return get_dispatcher(BotConfig(bot_token="--"))


async def bot_main():
    logger.info("start")
    bot = Bot(config.bot_token)
    await get_dispatcher(config).start_polling(bot)
