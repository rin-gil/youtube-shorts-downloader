"""Handles errors"""

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import TelegramAPIError

from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger

_ = i18n.gettext  # Alias for gettext method


async def errors_handler(update: Update, exception: TelegramAPIError) -> bool:
    """Logs exceptions that have occurred and are not handled by other functions"""
    message_from_user: str | None = None
    chat_id: int | None = None

    if update.message:
        user_lang_code: str = update.message.from_user.language_code
        chat_id = update.message.chat.id
        message_from_user = update.message.text
        await update.bot.send_message(
            chat_id=chat_id,
            text="❌ " + _("Unexpected error. We will fix it in the near future.", locale=user_lang_code),
        )

    logger.error(
        "When processing the update with id=%s there was a unhandled error: %s. Message text: %s.",
        update.update_id,
        repr(exception),
        message_from_user,
    )

    # Reset FSM state, if necessary
    dp: Dispatcher = Dispatcher.get_current()
    if await dp.storage.get_state(chat=chat_id) == "UserInput:Block":
        await dp.storage.reset_state(chat=chat_id, with_data=True)

    return True


def register_errors_handlers(dp: Dispatcher) -> None:
    """Registers errors handlers"""
    dp.register_errors_handler(errors_handler)
