import logging

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent

from diary_ms.application.common.exceptions.base import ApplicationError, InfraError
from diary_ms.domain.common.exceptions.base import DomainError, DomainValueError
from diary_ms.presentation.telegram.controllers.states import MainMenuSG

logger = logging.getLogger(__name__)
error_router = Router()


@error_router.errors(ExceptionTypeFilter(DomainValueError))
async def handle_domain_value_error(event: ErrorEvent):
    """
    Обработчик ошибок валидации Value Object.
    Срабатывает только на исключения типа DomainValueError.
    """
    error: DomainValueError = event.exception  # type: ignore
    update = event.update

    # Логируем с детализацией
    logger.warning(
        f"Ошибка валидации VO у пользователя {update.event.from_user.id}: "  # pyright: ignore[reportAttributeAccessIssue]
        f"{error} ({error.detail})"
    )

    # Формируем сообщение для пользователя
    base_message = str(error)
    user_message = f"❌ {base_message}"

    # Отправляем сообщение в зависимости от типа апдейта
    try:
        if update.message:
            await update.message.answer(user_message, parse_mode="HTML")
        elif update.callback_query:
            # Для callback показываем alert с ошибкой
            await update.callback_query.answer(
                user_message,
                show_alert=True,
                cache_time=10,  # Кешируем ответ на  10 секунд
            )
    except Exception as send_error:
        # Резервный вариант отправки, если с разметкой возникли проблемы
        logger.debug(f"Не удалось отправить сообщение с разметкой: {send_error}")
        fallback_message = f"Ошибка: {base_message}"
        if update.message:
            await update.message.answer(fallback_message)
        elif update.callback_query:
            await update.callback_query.answer(fallback_message, show_alert=True)
    # Не сбрасываем диалог — пользователь должен исправить ввод
    return True


@error_router.errors()
async def global_error_handler(event: ErrorEvent, dialog_manager: DialogManager):
    error = event.exception
    is_dialog_error: bool = isinstance(error, UnknownIntent | OutdatedIntent)
    if is_dialog_error:
        logger.warning(f"Ошибка состояния диалога: {type(error).__name__}")
    elif isinstance(error, ApplicationError):
        logger.warning(f"Ошибка в бизнес логике: {type(error).__name__}")
    elif isinstance(error, InfraError):
        logger.warning(f"Ошибка в инфраструктуре: {type(error).__name__}")
    elif isinstance(error, DomainError):
        logger.warning(f"Ошибка в домене: {type(error).__name__}")
    else:
        logger.warning(f"Неизвестная ошибка: {type(error).__name__}", exc_info=True)

    dialog_error_message: str = "🔄 Диалог устарел. Возвращаем в главное меню."
    unknown_error_message: str = "❌ ОШИБКА! Возвращаем в главное меню."

    # Уведомляем пользователя в зависимости от типа события
    if event.update.callback_query:
        # Это было нажатие кнопки
        await event.update.callback_query.answer(
            dialog_error_message if is_dialog_error else unknown_error_message,
            show_alert=False,  # Тихое уведомление
            cache_time=10,
        )

        # Пытаемся удалить сообщение с нерабочими кнопками
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()  # pyright: ignore[reportAttributeAccessIssue]
            except TelegramBadRequest:
                # Сообщение уже удалено или нет прав
                pass

    elif event.update.message:
        # Это было обычное сообщение
        await event.update.message.answer(
            dialog_error_message if is_dialog_error else unknown_error_message,
            reply_markup=ReplyKeyboardRemove(),  # Убираем клавиатуру
            cache_time=10,
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
