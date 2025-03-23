from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .diary_cards import states

start_router = Router()


@start_router.message(CommandStart())
async def start(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        states.CreateDiaryCardSG.mood,
        mode=StartMode.RESET_STACK,
    )
