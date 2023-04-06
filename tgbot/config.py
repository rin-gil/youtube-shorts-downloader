"""Configuration settings for the bot"""

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


_BASE_DIR: Path = Path(__file__).resolve().parent.parent
LOG_FILE: str = join(_BASE_DIR, "log.log")
BOT_LOGO: str = normpath(join(_BASE_DIR, "tgbot/assets/img/bot_logo.png"))
DB_FILE: str = normpath(join(_BASE_DIR, "tgbot/db.sqlite3"))
TEMP_DIR: str = normpath(join(_BASE_DIR, "tgbot/temp"))
LOCALES_DIR: str = normpath(join(_BASE_DIR, "tgbot/locales"))


class TgBot(NamedTuple):
    """Bot data"""

    token: str
    admin_ids: tuple[int, ...]


class Config(NamedTuple):
    """Bot config"""

    tg_bot: TgBot


def load_config(path: str | None) -> Config:
    """Loads settings from environment variables"""
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN"), admin_ids=tuple(map(int, env.list("ADMINS")))))
