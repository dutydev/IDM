from dutymanager.units.utils import *
from dutymanager.db.methods import AsyncDatabase
from module import Blueprint
from module.objects.types import ToGroup

bot = Blueprint(name="To Group")
db = AsyncDatabase.get_current()


@bot.event.to_group()
async def wrapper(event: ToGroup):
    peer_id = db.chats(event.object.chat)
    data = await get_by_local(peer_id, event.object.local_id)
    from_id = event.message.from_id
    if "reply_message" not in data:
        attachments = get_attachments(data)
        message = [""]
    else:
        attachments = get_attachments(data["reply_message"])
        message = [data["reply_message"]["text"]]
        from_id = data["reply_message"]["from_id"]

    if not any([message, attachments]):
        return send_msg(peer_id, "❗ Запись не может быть пустой.")

    if "автор" in event.message.text:
        message.append("\n\n🗣 Автор: [id{}|{}]".format(
            from_id, await get_name(from_id)
        ))

    await bot.api.wall.post(
        owner_id=-event.object.group_id,
        from_group=True,
        attachments=attachments,
        message="\n".join(message).replace("!вгр", ""),
        guid=0
    )
    return await send_msg(peer_id, "✅ Запись опубликована!")










