from dutymanager.db.methods import AsyncDatabase
from dutymanager.files.dicts import default_data
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.vk_script import msg_edit
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Friends worker")
db = AsyncDatabase.get_current()
worker = Worker.get_current()


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="друзья",
    lower=True
)
async def check_state(event: types.SendMySignal):
    message = "Автодобавление в друзья {}.".format(
        "работает"
        if db.settings("friends") else
        "не работает"
    )
    return await msg_edit(
        db.chats(event.object.chat),
        message,
        event.object.conversation_message_id
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="+друзья",
    lower=True
)
async def turn_on(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if db.settings("friends"):
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Автодобавление в друзья уже включено.",
        )
    if not default_data["friends_token"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Ошибка, не указан токен для этой функции."
        )
    await worker.manage_worker("friends", start=True)
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Автодобавление в друзья запущено!"
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="-друзья",
    lower=True
)
async def turn_off(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if not db.settings("friends"):
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Автодобавление в друзья и так отключено."
        )
    await worker.manage_worker("friends", start=False)
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Автодобавление в друзья отключено!"
    )
