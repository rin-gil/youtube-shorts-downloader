"""Configuration settings for the bot"""

from os.path import join
from pathlib import Path
from typing import NamedTuple, Optional

from environs import Env


_BASE_DIR: Path = Path(__file__).resolve().parent
LOG_FILE: str = join(_BASE_DIR, "YouTubeShortsDownloader.log")
BOT_LOGO: str = join(_BASE_DIR, "assets/img/bot_logo.png")
TEMP_DIR: str = join(_BASE_DIR, "temp")
LOCALES_DIR: str = join(_BASE_DIR, "locales")


class TgBot(NamedTuple):
    """Bot data"""

    token: str


class Config(NamedTuple):
    """Bot config"""

    tg_bot: TgBot


def load_config(path: Optional[str] = None) -> Config:
    """Loads settings from environment variables"""
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN")))
