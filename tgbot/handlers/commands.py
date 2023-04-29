"""Handles commands from user"""

from aiogram import Dispatcher
from aiogram.types import InputFile, Message

from tgbot.config import BOT_LOGO
from tgbot.middlewares.localization import i18n


_ = i18n.gettext  # Alias for gettext method


async def if_user_sent_command_start(message: Message) -> None:
    """Handles command /start from the user"""
    answer_text: str = "🔗 " + _("Send a link to YouTube Shorts", locale=message.from_user.language_code)
    await message.answer_photo(photo=InputFile(BOT_LOGO), caption=answer_text)


async def if_user_sent_command_about(message: Message) -> None:
    """Handles command /about from the user"""
    answer_text: str = "😉 " + _("I can download videos from YouTube Shorts", locale=message.from_user.language_code)
    await message.answer_photo(photo=InputFile(BOT_LOGO), caption=answer_text)


def register_commands_handlers(dp: Dispatcher) -> None:
    """Registers command handlers"""
    dp.register_message_handler(if_user_sent_command_start, commands=["start"], state=None)
    dp.register_message_handler(if_user_sent_command_about, commands=["about"], state=None)
