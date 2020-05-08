from dutymanager.units.vk_script import delete_messages
from dutymanager.db.methods import AsyncDatabase
from dutymanager.files.errors import VK_ERROR
from dutymanager.units.utils import *
from module import VKError, types
from module import Blueprint

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.event.delete_messages_from_user()
async def delete_from_user(event: types.DeleteMessagesFromUser):
    message_ids = []
    member_ids = event.object.member_ids
    peer_id = db.chats(event.object.chat)
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
        e = list(e.args)[0]
        await send_msg(peer_id, VK_ERROR.get(e, "❗ Произошла неизвестная ошибка."))


@bot.event.delete_messages()
async def _delete_messages(event: types.DeleteMessages):
    peer_id = db.chats(event.object.chat)
    local_ids = event.object.local_ids
    spam = event.object.is_spam
    try:
        await delete_messages(peer_id, local_ids, spam)
        await send_msg(peer_id, "✅ Сообщения удалены.")
    except VKError as e:
        e = list(e.args)[0]
        await send_msg(peer_id, VK_ERROR.get(e, "❗ Произошла неизвестная ошибка."))