"""

Built-in tools
for duty-manager.

"""

from dutymanager.files.dicts import default_data, intervals
from dutymanager.files.config import SETTINGS_PATH
from inspect import signature as sign
from module.utils import logger
from typing import Any, Optional

import json
import re


__all__ = (
    "display_time", "parse_interval",
    "load_values", "recreate",
    'get_values'
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


def get_values(cls, data: dict = None) -> dict:
    data = data or load_values()
    return {
        k: data[k]
        for k in sign(cls.__init__).parameters
        if k in data and k != "self"
    }


def update_fields(item: str, value: Any):
    default_data[item] = value
    try:
        with open(SETTINGS_PATH, mode="w") as file:
            file.write(json.dumps(default_data, indent=2))
            logger.debug("{} == {}", item, value)
    except FileNotFoundError:
        return recreate()


def load_values() -> Optional[dict]:
    copy = default_data.copy()
    default_data.clear()
    try:
        with open(SETTINGS_PATH) as file:
            default_data.update(**json.loads(file.read()))
            return default_data
    except FileNotFoundError:
        logger.error(
            "Can't find file \"settings.json\"! "
            "Reload script to recreate it."
        )
        return recreate(copy)


def recreate(data: dict = None):
    if data is None:
        data = default_data
    with open(SETTINGS_PATH, mode="w") as file:
        file.write(json.dumps(data, indent=2))
        logger.info("Recreated datafile \"settings.json\".")