import logging

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent

from src.diary_ms.application.common.exceptions.base import ApplicationError, InfraError
from src.diary_ms.domain.common.exceptions.base import DomainError
from src.diary_ms.presentation.telegram.controllers.states import MainMenuSG

logger = logging.getLogger(__name__)
error_router = Router()


@error_router.errors()
async def global_error_handler(event: ErrorEvent, dialog_manager: DialogManager):
    error = event.exception
    if isinstance(error, UnknownIntent | OutdatedIntent):
        logger.warning(f"Ошибка состояния диалога: {type(error).__name__}")
    elif isinstance(error, ApplicationError):
        logger.warning(f"Ошибка в бизнес логике: {type(error).__name__}")
    elif isinstance(error, InfraError):
        logger.warning(f"Ошибка в инфраструктуре: {type(error).__name__}")
    elif isinstance(error, DomainError):
        logger.warning(f"Ошибка в домене: {type(error).__name__}")
    else:
        logger.warning(f"Неизвестная ошибка: {type(error).__name__}", exc_info=True)

    # Уведомляем пользователя в зависимости от типа события
    if event.update.callback_query:
        # Это было нажатие кнопки
        await event.update.callback_query.answer(
            "🔄 Диалог устарел. Возвращаем в главное меню.",
            show_alert=False,  # Тихое уведомление
        )

        # Пытаемся удалить сообщение с нерабочими кнопками
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                # Сообщение уже удалено или нет прав
                pass

    elif event.update.message:
        # Это было обычное сообщение
        await event.update.message.answer(
            "🔄 Диалог устарел. Возвращаем в главное меню.",
            reply_markup=ReplyKeyboardRemove(),  # Убираем клавиатуру
        )

    # 2. Перезапускаем диалог с главного меню
    try:
        await dialog_manager.start(
            MainMenuSG.main,
            mode=StartMode.RESET_STACK,  # Полный сброс
            show_mode=ShowMode.SEND,  # Отправляем новым сообщением
        )
        logger.info(f"Диалог перезапущен для пользователя {event.update.event.from_user.id}")  # pyright: ignore[reportAttributeAccessIssue]
    except Exception as e:
        logger.error(f"Не удалось перезапустить диалог: {e}")
        if event.update.callback_query:
            await event.update.callback_query.message.answer("Нажмите /start чтобы начать заново.")  # pyright: ignore[reportOptionalMemberAccess]

    return True
