from module import Blueprint, Method
from module import types
from ..db.methods import AsyncDatabase
from ..units.utils import *

bot = Blueprint(name="Base")
db = AsyncDatabase.get_current()


@bot.on.event(Method.SUBSCRIBE_SIGNALS)
async def subscribe_signals(event: types.SubscribeSignals):
    print(event)


@bot.on.event(Method.BIND_CHAT)
async def bind_chat(event: types.BindChat):
    uid = event.object.chat
    if uid not in db.chats:
        chat_id = await get_chat(event.message.date)
        await db.create_chat(uid, chat_id)
    await send_msg(db.chats[uid], "Беседа распознана")
    return "ok"