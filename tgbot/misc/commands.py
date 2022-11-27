"""Sets commands for the bot"""

from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_default_commands(dp: Dispatcher) -> None:
    """Sets the bot default commands"""
    await dp.bot.set_my_commands(commands=[BotCommand(command="start", description="Start")])
