"""Message handlers for administrators"""

from os import remove as os_remove

from aiogram import Dispatcher
from aiogram.types import InputFile, Message

from tgbot.config import BOT_LOGO
from tgbot.middlewares.localization import i18n
from tgbot.services.database import database
from tgbot.services.statistics import get_path_to_statistics_graph

_ = i18n.gettext  # Alias for gettext method


async def if_admin_sent_command_stats(message: Message) -> None:
    """Shows statistics for administrators"""
    lang_code: str = message.from_user.language_code
    path_to_statistics_graph: str | None = await get_path_to_statistics_graph(
        downloads_data=await database.get_downloads_data(), locale=lang_code
    )
    if path_to_statistics_graph:
        await message.reply_photo(
            photo=InputFile(path_to_statistics_graph),
            caption="📊 " + _("Statistics of bot video downloads by months", locale=lang_code),
        )
        os_remove(path_to_statistics_graph)
    else:
        await message.reply_photo(
            photo=InputFile(BOT_LOGO), caption="❌ " + _("Error in plotting the graph", locale=lang_code)
        )


def register_admin_handlers(dp: Dispatcher) -> None:
    """Registers admin handlers"""
    dp.register_message_handler(if_admin_sent_command_stats, commands="stats", state="*", is_admin=True)
