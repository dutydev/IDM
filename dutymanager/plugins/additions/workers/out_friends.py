from dutymanager.files.dicts import default_data, workers_state
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Out friends worker")
db = AsyncDatabase.get_current()
worker = Worker.get_current()


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="автоотписка",
    lower=True
)
async def check_state(event: types.SendMySignal):
    message = "Автоотписка от исходящих заявок {}.".format(
        "включена"
        if workers_state["deleter"] else
        "отключена"
    )
    return await msg_edit(
        db.chats(event.object.chat),
        message,
        event.object.conversation_message_id
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="+автоотписка",
    lower=True
)
async def turn_on(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if workers_state["deleter"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Автоотписка уже включена.",
        )
    if not default_data["friends_token"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Ошибка, не указан токен для этой функции."
        )
    worker.manage_worker("deleter", start=True)
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Автоотписка запущена!"
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="-автоотписка",
    lower=True
)
async def turn_off(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if not workers_state["deleter"]:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Автоотписка и так отключена."
        )
    worker.manage_worker("friends", start=False)
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Автоотписка успешно отключена!"
    )
