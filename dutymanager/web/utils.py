import json
import re
from typing import Optional

from dutymanager.files.config import SETTINGS_PATH
from dutymanager.files.dicts import default_data
from dutymanager.web.objects import WebBlueprint

__all__ = (
    'bot',
    'read_values',
    'write_values',
    'get_user'
)

from module.utils import logger

bot = WebBlueprint()


async def get_user(login: str) -> Optional[dict]:
    regex_pattern = r'id([0-9]+)'
    data = re.findall(regex_pattern, login)
    if not data:
        regex_pattern = r'vk\.com\/([\w]+)'
        data = re.findall(regex_pattern, login)
        if not data:
            return None

    try:
        user = await bot.api.users.get(user_ids=data[0])
        return user[0].dict()
    except Exception as e:
        return None


def write_values(data: dict = None):
    if data is None:
        data = default_data.copy()
    with open(SETTINGS_PATH, mode="w") as file:
        file.write(json.dumps(data, indent=2))
        logger.info("Recreated datafile \"settings.json\".")
    return data


def read_values() -> Optional[dict]:
    data = default_data.copy()
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as file:
            data.update(**json.loads(file.read()))
            return data
    except FileNotFoundError:
        logger.error(
            "Can't find file \"settings.json\"! "
            "Reload script to recreate it."
        )
        return write_values(data)
