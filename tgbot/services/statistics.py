"""Functions for plotting downloads in the bot and saving the graph image"""

from asyncio import get_running_loop
from os import makedirs, path
from typing import NamedTuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure

from tgbot.config import STATS_BG_IMAGE, TEMP_DIR
from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger

_ = i18n.gettext  # Alias for gettext method


class DownloadsData(NamedTuple):
    """Represents a counter of downloads by months"""

    date: list[str]
    downloads_counter: list[int]


def _format_date(date: str, locale: str) -> str:
    """Returns the formatted date value in the user's local language"""
    month_in_user_local_language: dict[str, str] = {
        "01": _("Jan", locale=locale),
        "02": _("Feb", locale=locale),
        "03": _("Mar", locale=locale),
        "04": _("Apr", locale=locale),
        "05": _("May", locale=locale),
        "06": _("Jun", locale=locale),
        "07": _("Jul", locale=locale),
        "08": _("Aug", locale=locale),
        "09": _("Sep", locale=locale),
        "10": _("Oct", locale=locale),
        "11": _("Nov", locale=locale),
        "12": _("Dec", locale=locale),
    }
    return f"{month_in_user_local_language.get(date[5:])}\n{date[:4]}"


def plot_download_graph(downloads_data: DownloadsData, locale: str) -> str | None:
    """Builds an image of the download graph and saves it to a file"""
    try:
        figure: Figure = plt.figure(figsize=(8, 4.5))
        axes: Axes = figure.add_subplot()

        # Let's get the data for the graph
        downloads_counter: list[int] = downloads_data.downloads_counter
        dates: list[str] = [_format_date(date=date, locale=locale) for date in downloads_data.date]
        range_of_dates: range = range(len(dates))  # Number of values on the abscissa axis

        # Making a chart
        bar_container: BarContainer = axes.bar(range_of_dates, downloads_counter)
        axes.bar_label(container=bar_container)
        axes.invert_xaxis()

        # Add explanatory labels
        axes.set_title(label=_("Downloads chart by dates", locale=locale))
        axes.set_ylabel(ylabel=_("Number of downloads", locale=locale))
        axes.set_yticks([])  # Remove labels on the ordinate axis
        plt.xticks(range_of_dates, dates)  # Add the labels on the abscissa axis

        # Add background image on chart
        bg_image = plt.imread(fname=STATS_BG_IMAGE, format="png")
        x_min, x_max = axes.get_xlim()
        y_min, y_max = axes.get_ylim()
        axes.imshow(bg_image, extent=(x_min, x_max, y_min, y_max), aspect="auto", alpha=0.3)

        # Save the chart to a file
        path_to_statistics_graph: str = path.join(TEMP_DIR, "stats.png")
        figure.savefig(path.join(TEMP_DIR, "stats.png"))

        return path_to_statistics_graph

    except Exception as ex:
        logger.info("Error in plotting the graph: %s", ex)

    return None


async def get_path_to_statistics_graph(downloads_data: DownloadsData, locale: str) -> str | None:
    """Returns the path to the graph image"""
    if not path.exists(TEMP_DIR):
        makedirs(TEMP_DIR)
    path_to_graph_image: str | None = await get_running_loop().run_in_executor(
        None, plot_download_graph, downloads_data, locale
    )
    return path_to_graph_image
