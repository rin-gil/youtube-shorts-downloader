"""Set of functions for working with YouTube"""

from os.path import join
from typing import Any, NamedTuple

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from tgbot.config import TEMP_DIR
from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger
from tgbot.services.decorators import run_in_asyncio_thread

_ = i18n.gettext  # Alias for gettext method


class VideoInfo(NamedTuple):
    """Presents information about the video"""

    description: str
    url: str


class YouTube:
    """Describes methods for working with YouTube videos"""

    @staticmethod
    def _remove_unwanted_chars(string: str) -> str:
        """Removes everything from the string except letters, numbers, spaces, hyphens, and underscores"""
        processed_string: str = ""
        for char in string[:100]:
            if char.isalnum() or char == "-" or char == "_":
                processed_string += char
            elif char.isspace() and (not processed_string or not processed_string[-1].isspace()):
                processed_string += char
        return processed_string

    @run_in_asyncio_thread
    def download_video(self, youtube_watch_url: str) -> Any:
        """
        Downloads the best video stream from the YouTube Shorts link

        Note: Do not use named arguments when calling this method

        Args:
            youtube_watch_url (): link to YouTube Shorts video

        Returns:
            The path to the uploaded video file, or None if the original video file is a live broadcast
        """
        options: dict = {
            "format": "best",
            "geo_bypass": True,
            "noplaylist": True,
            "noprogress": True,
            "quiet": True,
        }
        ydl: YoutubeDL = YoutubeDL(params=options)

        try:
            # Getting information about the video
            video_info = ydl.extract_info(youtube_watch_url, download=False)
            duration: int | None = video_info.get("duration")

            if duration and duration <= 60:
                # Set save folder and file name
                title: str = video_info.get("title")
                path_to_file: str = join(TEMP_DIR, f"{self._remove_unwanted_chars(string=title)}.mp4")
                params: dict = getattr(ydl, "params")
                params.update({"outtmpl": {"default": path_to_file}})
                setattr(ydl, "params", params)

                # Load a video stream
                ydl.download(youtube_watch_url)

                return f"{path_to_file}"

        except YoutubeDLError as ex:
            logger.error("Error when loading video: %s", repr(ex))

        return None


youtube = YouTube()
