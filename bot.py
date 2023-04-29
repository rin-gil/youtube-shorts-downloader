"""Launches the bot"""

from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin_handlers
from tgbot.handlers.commands import register_commands_handlers
from tgbot.handlers.error import register_errors_handlers
from tgbot.handlers.messages import register_messages_handlers
from tgbot.middlewares.localization import i18n
from tgbot.misc.commands import set_default_commands
from tgbot.misc.logger import logger
from tgbot.services.database import database


def register_all_middlewares(dp: Dispatcher) -> None:
    """Registers middlewares"""
    dp.middleware.setup(i18n)


def register_all_filters(dp: Dispatcher) -> None:
    """Registers filters"""
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher) -> None:
    """Registers handlers"""
    register_admin_handlers(dp)
    register_commands_handlers(dp)
    register_messages_handlers(dp)
    register_errors_handlers(dp)


async def main() -> None:
    """Launches the bot"""
    config: Config = load_config(path=".env")
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
    bot["config"] = config
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    try:  # On starting bot
        await database.init()
        await set_default_commands(dp)
        await dp.skip_updates()
        await dp.start_polling()
    finally:  # On stopping bot
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    logger.info("Starting bot")
    try:
        run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        logger.critical("Unknown error: %s", repr(ex))
    logger.info("Bot stopped!")
