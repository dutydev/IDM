from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import send_msg
from module import Blueprint, Method
from module import types

bot = Blueprint()
db = AsyncDatabase.get_current()


async def unbind_chat(uid: str):
    if uid in db.chats:
        data = await db.chats.remove(uid)
        await send_msg(data["id"], "✅ Чат «{}» успешно отвязан.".format(
            data.get("title", "null")
        ))


@bot.event.message_signal(
    Method.SEND_SIGNAL,
    text=["отвязать", "отвязать <uid>"]
)
async def send_signal(event: types.SendSignal, uid: str = None):
    uid = uid if uid else event.object.chat
    if event.object.from_id in db.trusted:
        await unbind_chat(uid)


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=["отвязать", "отвязать <uid>"]
)
async def send_my_signal(event: types.SendMySignal, uid: str = None):
    uid = uid if uid else event.object.chat
    await unbind_chat(uid)
