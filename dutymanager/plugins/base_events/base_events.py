from module import Blueprint, Method
from module import VKError, types
from const import errors
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import *

bot = Blueprint(name="Base")
db = AsyncDatabase.get_current()


@bot.on.event(Method.PRINT_BOOKMARK)
async def print_bookmark(event: types.PrintBookmark):
    peer_id = db.chats[event.object.chat]
    local_id = event.object.conversation_message_id
    description = event.object.description
    try:
        await send_msg(
            peer_id,
            f"🔼 Перейти к закладке «{description}»",
            reply_to=(await get_by_local(peer_id, local_id))["id"]
        )
    except (IndexError, VKError) as e:
        e = list(e.args)[0][0]
        await send_msg(peer_id, errors.get(e, "❗ Произошла неизвестная ошибка."))


@bot.on.event(Method.BAN_GET_REASON)
async def ban_get_reason(event: types.BanGetReason):
    peer_id = db.chats[event.object.chat]
    local_id = event.object.local_id
    try:
        await send_msg(
            peer_id,
            "🔼 Перейти к месту бана",
            reply_to=(await get_by_local(peer_id, local_id))["id"]
        )
    except (IndexError, VKError) as e:
        e = list(e.args)[0][0]
        await send_msg(peer_id, errors.get(e, "❗ Произошла неизвестная ошибка."))


async def abstract_bind(uid: str, text: str, date: int):
    if uid not in db.chats:
        chat_id = await get_chat(date, text)
        await db.create_chat(uid, chat_id)
    await send_msg(db.chats[uid], "✅ Беседа распознана")


@bot.on.event(Method.BIND_CHAT)
async def bind_chat(event: types.BindChat):
    await abstract_bind(
        uid=event.object.chat,
        text="!связать",
        date=event.message.date
    )


@bot.on.event(Method.SUBSCRIBE_SIGNALS)
async def subscribe_signals(event: types.SubscribeSignals):
    await abstract_bind(
        uid=event.object.chat,
        text=event.object.text,
        date=event.message.date
    )