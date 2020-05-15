from module.objects.types import DeleteMessages, DeleteMessagesFromUser
from dutymanager.units.vk_script import delete_messages
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import *
from module import Blueprint
from time import time

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.event.delete_messages_from_user()
async def delete_from_user(event: DeleteMessagesFromUser):
    message_ids = []
    member_ids = event.object.member_ids
    peer_id = db.chats(event.object.chat)
    for i in await get_history(peer_id):
        if i["from_id"] in member_ids and "action" not in i:
            if (time() - i["date"]) < 86400:  # Вложенные if`ы - зло (noqa)
                message_ids.append(str(i["id"]))
    if not message_ids:
        return await send_msg(peer_id, "❗ Сообщения не найдены.")

    await bot.api.messages.delete(
        message_ids=",".join(message_ids[:event.object.amount]),
        delete_for_all=True,
        spam=event.object.is_spam
    )
    await send_msg(peer_id, "✅ Сообщения удалены.")


@bot.event.delete_messages()
async def _delete_messages(event: DeleteMessages):
    peer_id = db.chats(event.object.chat)
    local_ids = event.object.local_ids
    spam = event.object.is_spam
    return await delete_messages(peer_id, local_ids, spam)
