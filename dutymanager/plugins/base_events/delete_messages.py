from module import Blueprint, Method
from module import VKError, types
from const import errors
from dutymanager.units.utils import *
from dutymanager.db.methods import AsyncDatabase

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.on.event(Method.DELETE_MESSAGES_FROM_USER)
async def delete_from_user(event: types.DeleteMessagesFromUser):
    message_ids = []
    member_ids = event.object.member_ids
    peer_id = db.chats[event.object.chat]
    for i in await get_history(peer_id):
        if i["from_id"] in member_ids and "action" not in i:
            if len(member_ids) < event.object.amount:
                message_ids.append(str(i["id"]))
            else:
                break
    if not message_ids:
        return await send_msg(peer_id, "❗ Сообщения не найдены.")
    try:
        await bot.api.messages.delete(
            message_ids=",".join(message_ids),
            delete_for_all=True,
            spam=event.object.is_spam
        )
        await send_msg(peer_id, "✅ Сообщения удалены.")
    except VKError as e:
        e = list(e.args)[0][0]
        await send_msg(peer_id, errors.get(e, "❗ Произошла неизвестная ошибка."))


@bot.on.event(Method.DELETE_MESSAGES)
async def delete_messages(event: types.DeleteMessages):
    peer_id = db.chats[event.object.chat]
    local_ids = event.object.local_ids
    message_ids = await get_msg_ids(peer_id, local_ids)
    if not message_ids:
        return await send_msg(peer_id, "❗ Сообщения не найдены.")

    try:
        await bot.api.messages.delete(
            ",".join(message_ids),
            delete_for_all=True,
            spam=event.object.is_spam
        )
        await send_msg(peer_id, "✅ Сообщения удалены.")
    except VKError as e:
        e = list(e.args)[0][0]
        await send_msg(peer_id, errors.get(e, "❗ Произошла неизвестная ошибка."))

