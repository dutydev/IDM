from dutymanager.files.errors import UNBIND_CHAT, VK_ERROR
from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import send_msg
from module import VKError
from module import Blueprint
from module.utils import logger
from traceback import format_exc

bot = Blueprint(name="Error Handler")
db = AsyncDatabase.get_current()


@bot.error_handler(VKError)
async def swear(e: VKError, event: dict):
    """
    Абстрактная функция, которая ловит ошибки от VK.
    Сделана для того, чтобы не оборачивать каждый
    хэндлер в try/except блоки.
    :param e: Класс ошибки (VKError)
    :param event: Пришедший эвент/сигнал
    """
    logger.error(format_exc(5))
    if event["method"] in ("ping", "banExpired"):
        return
    uid = event["object"]["chat"]
    if uid not in db.chats:
        return {"response": "error", "error_code": UNBIND_CHAT}

    if event["object"].get("from_id") == bot.user_id:
        return await msg_edit(
            db.chats(uid),
            f"❗ {VK_ERROR.get(e.error_code)}",
            event["message"]["conversation_message_id"]
        )
    return await send_msg(
        db.chats(uid), f"❗ {VK_ERROR.get(e.error_code)}"
    )
