"""

Built-in tools
for duty-manager.

"""

from ..core.config import default_data, intervals
from dutymanager.units.const import SETTINGS_PATH
from module.utils import logger
from typing import Any

import json
import re


__all__ = (
    "display_time", "parse_interval",
    "load_values", "recreate",
)


def display_time(seconds: int) -> str:
    result = []

    for name, count in list(intervals.items()):
        value = int(seconds // count)
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return '. '.join(result[:3])


def parse_interval(text: str) -> int:
    """ Парсинг ключевых слов (день, час, мин, сек ...)
    в секунды.
    :param text: -> string
    :return: unix (total seconds)
    """
    unix = 0
    tags = re.findall(r'(\d+)[. ](день|дн|час|мин|сек|)', text)
    for k, v in tags:
        unix += int(k) * intervals[v]
    return unix


def update_fields(item: str, value: Any):
    default_data[item] = value
    try:
        with open(SETTINGS_PATH, mode="w") as file:
            file.write(json.dumps(default_data, indent=2))
            logger.debug("{} == {}", item, value)
    except FileNotFoundError:
        recreate()


def load_values():
    copy = default_data.copy()
    default_data.clear()
    try:
        with open(SETTINGS_PATH) as file:
            dumps = json.loads(file.read())
            default_data.update(**dumps)
    except FileNotFoundError:
        logger.warning(
            "Can't find file \"settings.json\"! "
            "Reload script to recreate it."
        )
        recreate(copy)


def recreate(data: dict = None):
    if data is None:
        data = default_data
    with open(SETTINGS_PATH, mode="w") as file:
        file.write(json.dumps(data, indent=2))
        logger.info("Recreated datafile \"settings.json\".")