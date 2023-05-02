"""Handles messages from user"""

from os import remove as os_remove

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentTypes, InputFile, Message

from tgbot.middlewares.localization import i18n
from tgbot.misc.states import UserInput
from tgbot.services.database import database
from tgbot.services.youtube import youtube

_ = i18n.gettext  # Alias for gettext method


async def if_user_sent_link(message: Message) -> None:
    """Handles the message if a user sent YouTube link"""
    await database.increase_downloads_counter()
    lang_code: str = message.from_user.language_code
    chat_id: int = message.chat.id
    bot_reply: Message = await message.reply(text="⏳ " + _("Wait, downloading...", locale=lang_code))
    await UserInput.Block.set()  # Block user input while the download is in progress
    path_to_mp4_file: str | None = await youtube.download_video(message.text)
    if path_to_mp4_file:
        await message.reply_video(InputFile(path_to_mp4_file))
        await message.bot.delete_message(chat_id=chat_id, message_id=bot_reply.message_id)
        os_remove(path_to_mp4_file)
    else:
        await message.bot.edit_message_text(
            text="❌ "
            + _("Unable to download this video", locale=lang_code)
            + "\n\n"
            + _("Possible reasons:", locale=lang_code)
            + "\n"
            + "  - "
            + _("video is unavailable", locale=lang_code)
            + "\n"
            + "  - "
            + _("video with limited access", locale=lang_code),
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
        if_user_sent_link,
        Text(startswith="https://"),
        regexp=r"(?:https?://)?(?:www\.)?" r"(?:youtube.com/shorts/)" r"([a-zA-Z0-9_-]{11})",
        state=None,
    )
    dp.register_message_handler(if_user_sent_text, content_types=ContentTypes.TEXT, state=None)
    dp.register_message_handler(if_user_input_block, content_types=ContentTypes.TEXT, state=UserInput.Block)
    dp.register_message_handler(if_user_sent_anything_but_text, content_types=ContentTypes.ANY)
