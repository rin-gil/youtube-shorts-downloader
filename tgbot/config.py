"""Configuration settings for the bot"""

from os.path import join
from pathlib import Path
from typing import NamedTuple, Optional

from environs import Env


BASE_DIR: Path = Path(__file__).resolve().parent
LOG_FILE: str = join(BASE_DIR, "tgbot.log")


class DbConfig(NamedTuple):
    """Database configuration"""

    host: str
    password: str
    user: str
    database: str


class TgBot(NamedTuple):
    """Bot data"""

    token: str
    admin_ids: tuple[int, ...]


class Miscellaneous(NamedTuple):
    """Other settings"""

    other_params: Optional[str] = None


class Config(NamedTuple):
    """Bot config"""

    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: Optional[str] = None) -> Config:
    """Loads settings from environment variables"""
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=tuple(map(int, env.list("ADMINS"))),
        ),
        db=DbConfig(
            host=env.str("DB_HOST"), password=env.str("DB_PASS"), user=env.str("DB_USER"), database=env.str("DB_NAME")
        ),
        misc=Miscellaneous(),
    )
