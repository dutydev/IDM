from dutymanager.files.dicts import default_data, workers_state
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Eternal online worker")
db = AsyncDatabase.get_current()
worker = Worker.get_current()


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="онлайн",
    lower=True
)
async def check_state(event: types.SendMySignal):
    message = "Вечный онлайн {}.".format(
        "включен"
        if workers_state["online"] else
        "отключен"
    )
    return await msg_edit(
        db.chats(event.object.chat),
        message,
        event.object.conversation_message_id
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="+онлайн",
    lower=True
)
async def turn_on(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if workers_state["online"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Вечный онлайн уже запущен."
        )

    if not default_data["online_token"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Ошибка, не указан токен для этой функции."
        )
    worker.manage_worker("online", start=True)
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Вечный онлайн запущен!"
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="-онлайн",
    lower=True
)
async def turn_off(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if not workers_state["online"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Вечный онлайн и так отключен."
        )
    worker.manage_worker("online", start=False)
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Вечный онлайн отключен."
    )
