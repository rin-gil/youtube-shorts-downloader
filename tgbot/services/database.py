"""Functions for working with the database"""

from datetime import datetime
from sqlite3 import OperationalError
from sys import exit as sys_exit

from aiosqlite import connect

from tgbot.config import DB_FILE
from tgbot.misc.logger import logger
from tgbot.services.statistics import DownloadsData


async def database_init() -> None:
    """Creates a database file and a table in it"""
    try:
        async with connect(database=DB_FILE) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS downloads_counters (
                    date VARCHAR(7) PRIMARY KEY,
                    counter INTEGER NOT NULL DEFAULT 0
                );
                """
            )
    except OperationalError as ex:
        logger.critical("Database connection error: %s", ex)
        sys_exit()


async def get_downloads_data() -> DownloadsData:
    """Returns the number of YouTube Shorts uploads made by the bot in the last 12 months"""
    dates: list = []
    downloads: list = []
    async with connect(database=DB_FILE) as db:
        async with db.execute(
            """
            SELECT date, counter
            FROM downloads_counters
            ORDER BY date DESC
            LIMIT 12;
            """
        ) as cursor:
            async for row in cursor:
                dates.append(row[0])
                downloads.append(row[1])
    return DownloadsData(date=dates, downloads_counter=downloads)


async def increase_downloads_counter() -> None:
    """Increases the value of the YouTube Shorts download counter"""
    async with connect(database=DB_FILE) as db:
        await db.execute(
            """
            INSERT INTO downloads_counters (date, counter) VALUES (?, ?)
            ON CONFLICT (date) DO UPDATE SET counter=counter+1;
            """,
            (datetime.now().strftime("%Y.%m"), 1),
        )
        await db.commit()
