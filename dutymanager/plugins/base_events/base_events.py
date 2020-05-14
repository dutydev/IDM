from dutymanager.units.vk_script import get_chat, msg_edit
from dutymanager.files.errors import CANT_BIND_CHAT
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.vk_script import msg_send
from tortoise.exceptions import BaseORMException
from module.utils import logger
from module import Blueprint
from module import types

bot = Blueprint(name="Base")
db = AsyncDatabase.get_current()


@bot.event.print_bookmark()
async def print_bookmark(event: types.PrintBookmark):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    description = event.object.description
    await msg_send(
        peer_id=peer_id, local_id=local_id,
        message=f"🔼 Перейти к закладке «{description}»"
    )


@bot.event.ban_get_reason()
async def ban_get_reason(event: types.BanGetReason):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.local_id
    await msg_send(peer_id, "🔼 Перейти к месту бана", local_id)


async def abstract_bind(
    uid: str, text: str, local_id: int
):
    if uid not in db.chats:
        chat_id, title = await get_chat(local_id, text)
        return await db.chats.create(uid, chat_id, title)
    await msg_edit(
        peer_id=db.chats(uid), local_id=local_id,
        message=f"✅ Беседа «{db.chats(uid, 'title')}» распознана!",
    )


@bot.event.bind_chat()
async def bind_chat(event: types.BindChat):
    return await abstract_bind(
        event.object.chat,
        "!связать",
        event.message.conversation_message_id
    )


@bot.event.subscribe_signals()
async def subscribe_signals(event: types.SubscribeSignals):
    uid = event.object.chat
    try:
        await abstract_bind(
            uid,
            event.object.text,
            event.message.conversation_message_id
        )
        await db.chats.change(uid, is_duty=True)
    except (BaseORMException, Exception) as e:
        logger.error(e)
        return {"response": "error", "error_code": CANT_BIND_CHAT}