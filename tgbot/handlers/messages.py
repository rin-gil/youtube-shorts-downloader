"""Handles messages from user"""

from os import remove as os_remove

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentTypes, InputFile, Message

from tgbot.middlewares.localization import i18n
from tgbot.misc.states import UserInput
from tgbot.services.database import increase_downloads_counter
from tgbot.services.youtube import get_path_to_video_file

_ = i18n.gettext  # Alias for gettext method


async def if_user_sent_link(message: Message) -> None:
    """Handles the message if a user sent YouTube link"""
    lang_code: str = message.from_user.language_code
    chat_id: int = message.chat.id
    bot_reply: Message = await message.reply(text="⏳ " + _("Wait, downloading...", locale=lang_code))
    await UserInput.Block.set()  # Block user input while the download is in progress
    path_to_mp4_file: str | None = await get_path_to_video_file(url=message.text)
    if path_to_mp4_file:
        await message.reply_video(InputFile(path_to_mp4_file))
        await message.bot.delete_message(chat_id=chat_id, message_id=bot_reply.message_id)
        os_remove(path_to_mp4_file)
        await increase_downloads_counter()
    else:
        await message.bot.edit_message_text(
            text="❌ " + _("Unable to download this video", locale=lang_code),
            chat_id=chat_id,
            message_id=bot_reply.message_id,
        )
    await UserInput.previous()  # Unblock user input, when download completed


async def if_user_sent_text(message: Message) -> None:
    """Handles the message if a user sent text"""
    await message.reply(text="❌ " + _("This is not a link to YouTube Shorts", locale=message.from_user.language_code))


async def if_user_input_block(message: Message) -> None:
    """Deletes all user messages in the UserInput.Block state"""
    await message.delete()


async def if_user_sent_anything_but_text(message: Message) -> None:
    """Deletes messages with any content from a user that is not text"""
    await message.delete()


def register_messages_handlers(dp: Dispatcher) -> None:
    """Registers command handlers"""
    dp.register_message_handler(
        if_user_sent_link, Text(startswith="https://"), regexp=r"(?:shorts\/)([0-9A-Za-z_-]{11}).*", state=None
    )
    dp.register_message_handler(if_user_sent_text, content_types="text", state=None)
    dp.register_message_handler(if_user_input_block, content_types="text", state=UserInput.Block)
    dp.register_message_handler(if_user_sent_anything_but_text, content_types=ContentTypes.ANY, state="*")
