"""Launches the bot"""

from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.misc.commands import set_default_commands
from tgbot.misc.logger import log


def register_all_filters(dp: Dispatcher) -> None:
    """Registers filters"""
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher) -> None:
    """Registers handlers"""
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def main() -> None:
    """Launches the bot"""
    config: Config = load_config(path=".env")
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
    bot["config"] = config
    register_all_filters(dp)
    register_all_handlers(dp)
    try:  # On starting bot
        await set_default_commands(dp)
        await dp.skip_updates()
        await dp.start_polling()
    finally:  # On stopping bot
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    log.info("Starting bot")
    try:
        run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as ex:
        log.critical("Unknown error: %s", ex)
    log.info("Bot stopped!")
