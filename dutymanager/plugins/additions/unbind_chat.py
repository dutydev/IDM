from module import Blueprint, Method
from module import types
from dutymanager.units.utils import send_msg
from dutymanager.db.methods import AsyncDatabase

bot = Blueprint()
db = AsyncDatabase.get_current()


async def unbind_chat(uid: str):
    if uid in db.chats:
        chat_id = await db.remove_chat(uid)
        await send_msg(chat_id, "✅ Чат успешно отвязан.")


@bot.on.message_event(
    Method.SEND_SIGNAL,
    text=["отвязать", "отвязать <uid>"]
)
async def send_signal(event: types.SendSignal, uid: str = None):
    uid = uid if uid else event.object.chat
    await unbind_chat(uid)


@bot.on.message_event(
    Method.SEND_MY_SIGNAL,
    text=["отвязать", "отвязать <uid>"]
)
async def send_my_signal(event: types.SendMySignal, uid: str = None):
    uid = uid if uid else event.object.chat
    await unbind_chat(uid)
