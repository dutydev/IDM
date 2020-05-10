from dutymanager.files.dicts import default_data, workers_state
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Friends worker")
db = AsyncDatabase.get_current()
worker = Worker.get_current()


@bot.on.message_handler(Method.SEND_MY_SIGNAL)
async def turn_on(event: types.SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if workers_state["friends"]:
        return msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="Автодобавление в друзья уже включено.",
        )
    if not default_data["friends_token"]:
        return msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="Ошибка! Не указан токен для этой функции."
        )
    worker.run_worker("friends")
    return msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="Автодобавление в друзья запущено!"
    )