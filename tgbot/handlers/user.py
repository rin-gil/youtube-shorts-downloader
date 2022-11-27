"""Handles start command from user"""

from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message) -> None:
    """Handles start command from user"""
    await message.reply("Hello, user!")


def register_user(dp: Dispatcher) -> None:
    """Registers command handlers"""
    dp.register_message_handler(user_start, commands=["start"], state="*")
