from dutymanager.files.errors import UNBIND_CHAT, VK_ERROR
from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import send_msg
from module import VKError
from module import Blueprint
from module.utils import logger
from traceback import format_exc
from asyncio import sleep
from re import findall

bot = Blueprint(name="Error Handler")
db = AsyncDatabase.get_current()

MESSAGE = """❗ Произошла ошибка.
Метод: {method}
ВК Ответил: {description} ({code})."""


async def rps_handler(e: VKError):
    await sleep(1)
    return await e.method_requested(**e.params_requested)


@bot.error_handler(KeyError)
async def key_error(e: KeyError, event: dict):
    if findall("[0-9a-zA-Z]{8}", str(e)):
        logger.error(
            "Чат {} всё еще не был связан.",
            event["object"]["chat"]
        )
        return {"response": "error", "error_code": UNBIND_CHAT}
    logger.error(format_exc(5))


@bot.error_handler(VKError)
async def swear(e: VKError, event: dict):
    """
    Абстрактная функция, которая ловит ошибки от VK.
    Сделана для того, чтобы не оборачивать каждый
    хэндлер в try/except блоки.
    :param e: Класс ошибки (VKError)
    :param event: Пришедший эвент/сигнал
    """
    if e.error_code == 6:
        return await rps_handler(e)
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
    await send_msg(
        db.chats(uid), MESSAGE.format(
            method=event["method"],
            description=e.error_description,
            code=e.error_code
        )
    )
    return {"response": "error", "error_code": e.error_code}