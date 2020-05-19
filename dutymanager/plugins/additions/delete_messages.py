from dutymanager.units.vk_script import (
    generate_history,
    delete_messages,
    msg_edit
)
from dutymanager.units.tools import display_time
from dutymanager.units.utils import send_msg
from dutymanager.db.methods import AsyncDatabase
from module.objects.types import SendMySignal
from module import Blueprint, Method
from time import time

bot = Blueprint(name="Delete self messages")
db = AsyncDatabase.get_current()


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=["-смс <num:int>", "-смс"]
)
async def delete_by_count(event: SendMySignal, num: int = 5000):
    peer_id = db.chats(event.object.chat)
    history = await generate_history(
        peer_id=peer_id,
        offset_max=(200, 5000)[num >= 200]
    )
    await send_msg(peer_id, "✅ Сообщения ({}) удалены.".format(
        await delete_messages([
            i["id"] for i in history if i["from_id"] == bot.user_id
            and "action" not in i
            and time() - i["date"] < 86400
        ][:num + 1]) - 1
    ))


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=["-смс <unix:unix>", "-смс за <unix:unix>"]
)
async def delete_by_time(event: SendMySignal, unix: int):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if unix >= 86400:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Невозможно удалить сообщения за такой срок."
        )
    history = await generate_history(
        peer_id=peer_id,
        offset_max=(200, 5000)[unix >= 7200]
    )
    count = await delete_messages([
            i["id"] for i in history if i["from_id"] == bot.user_id
            and "action" not in i
            and time() - i["date"] < unix
        ])
    await send_msg(peer_id, "✅ Удалено ({}) сообщений за {}.".format(
        count, display_time(unix)
    ))
