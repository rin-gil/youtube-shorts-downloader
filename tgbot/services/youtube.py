"""Functions for downloading videos from YouTube"""

from asyncio import get_running_loop, sleep
from typing import Any, Callable

from pytube import Stream, YouTube
from pytube.exceptions import PytubeError

from tgbot.config import TEMP_DIR
from tgbot.misc.logger import logger


def retry(max_retries: int) -> Callable:
    """A decorator that calls a function and, if an exception occurs, calls it again up to max_retries times"""

    def retry_decorator(func: Callable) -> Callable:
        """Internal decorator function that wraps the decorated asynchronous function"""

        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            A wrapped asynchronous function that catches a KeyError exception and, if it occurs, calls
            the decorated function, up to max_retries times
            """
            retries: int = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except KeyError:
                    retries += 1
                    await sleep(1)
            return None

        return wrapper

    return retry_decorator


def _remove_unwanted_chars(string: str) -> str:
    """Removes everything from the string except letters, numbers, spaces, hyphens, and underscores"""
    processed_string: str = ""
    for char in string[:100]:
        if char.isalnum() or char == "-" or char == "_":
            processed_string += char
        elif char.isspace() and (not processed_string or not processed_string[-1].isspace()):
            processed_string += char
    return processed_string


def download_video(url: str) -> str | None:
    """Downloads videos from YouTube via a link"""
    try:
        youtube_video: YouTube = YouTube(url=url)
        video_stream: Stream = youtube_video.streams.get_highest_resolution()
        path_to_mp4_file: str = video_stream.download(
            output_path=TEMP_DIR, filename=f"{_remove_unwanted_chars(string=youtube_video.title)}.mp4"
        )
        return path_to_mp4_file
    except PytubeError as ex:
        logger.info("Error downloading video: %s", ex)
    return None


@retry(max_retries=10)
async def get_path_to_video_file(url: str | None) -> str | None:
    """Returns the path to the downloaded audio file"""
    path_to_mp4_file: str | None = await get_running_loop().run_in_executor(None, download_video, url)
    return path_to_mp4_file
