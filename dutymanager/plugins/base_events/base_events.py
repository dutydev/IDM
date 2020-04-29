from module import Blueprint
from module import VKError, types
from dutymanager.units.const import errors
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.vk_script import msg_send
from dutymanager.units.utils import *

bot = Blueprint(name="Base")
db = AsyncDatabase.get_current()


@bot.event.print_bookmark()
async def print_bookmark(event: types.PrintBookmark):
    peer_id = db.chats[event.object.chat]
    local_id = event.object.conversation_message_id
    description = event.object.description
    try:
        await msg_send(
            peer_id,
            f"🔼 Перейти к закладке «{description}»",
            local_id
        )
    except (IndexError, VKError) as e:
        e = list(e.args)[0][0]
        await send_msg(peer_id, errors.get(e, "❗ Произошла неизвестная ошибка."))


@bot.event.ban_get_reason()
async def ban_get_reason(event: types.BanGetReason):
    peer_id = db.chats[event.object.chat]
    local_id = event.object.local_id
    try:
        await msg_send(peer_id, "🔼 Перейти к месту бана", local_id)
    except (IndexError, VKError) as e:
        print(e)
        e = list(e.args)[0][0]
        await send_msg(peer_id, errors.get(e, "❗ Произошла неизвестная ошибка."))


async def abstract_bind(uid: str, text: str, date: int):
    if uid not in db.chats:
        chat_id = await get_chat(date, text)
        await db.create_chat(uid, chat_id)
    await send_msg(db.chats[uid], "✅ Беседа распознана")


@bot.event.bind_chat()
async def bind_chat(event: types.BindChat):
    await abstract_bind(
        uid=event.object.chat,
        text="!связать",
        date=event.message.date
    )


@bot.event.subscribe_signals()
async def subscribe_signals(event: types.SubscribeSignals):
    await abstract_bind(
        uid=event.object.chat,
        text=event.object.text,
        date=event.message.date
    )