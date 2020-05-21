import re

from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import send_msg
from module import Blueprint, VKError
from traceback import format_exc
from module.utils import logger
from typing import Optional

bot = Blueprint(name="Error Handler")
db = AsyncDatabase.get_current()

MESSAGE = """❗ Произошла ошибка.
Метод: {method}
ВК Ответил: {description} ({code})."""


@bot.error_handler(KeyError)
async def key_error(e: KeyError, event: dict):
    if re.findall("[0-9a-zA-Z]{8}", str(e)):
        logger.error(
            "Чат {} всё еще не был связан.",
            event["object"]["chat"]
        )
        return {"response": "error", "error_code": 4}


@bot.error_handler(VKError)
async def swear(e: VKError, event: dict) -> Optional[dict]:
    if event["method"] in ("ping", "banExpired"):
        return
    uid = event["object"]["chat"]
    if uid not in db.chats:
        return {"response": "error", "error_code": 4}

    message = MESSAGE.format(
        method=event["method"],
        description=e.error_description,
        code=e.error_code
    )
    if event["object"].get("from_id") == bot.user_id:
        return await msg_edit(
            db.chats(uid),
            message,
            event["message"]["conversation_message_id"]
        )
    await send_msg(db.chats(uid), message)
    return {
        "response": "vk_error",
        "error_message": e.error_description,
        "error_code": e.error_code
    }
