"""Handling messages from bot admins"""

from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start(message: Message) -> None:
    """Handles start command from admin"""
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher) -> None:
    """Registers command handlers"""
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
