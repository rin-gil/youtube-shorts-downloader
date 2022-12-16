"""Functions for downloading videos from YouTube"""

from asyncio import get_running_loop

from pytube import Stream, YouTube
from pytube.exceptions import PytubeError

from tgbot.config import TEMP_DIR
from tgbot.misc.logger import logger


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
    """
    Downloads videos from YouTube via a link

    :param url: link to YouTube Shorts video
    :return: path to downloaded mp4 file or None
    """
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


async def get_path_to_video_file(url: str | None) -> str | None:
    """Returns the path to the downloaded audio file"""
    path_to_mp4_file: str | None = await get_running_loop().run_in_executor(None, download_video, url)
    return path_to_mp4_file
