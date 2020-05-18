from dutymanager.units.utils import *
from dutymanager.db.methods import AsyncDatabase
from module import Blueprint
from module.objects.types import ToGroup
from typing import List

bot = Blueprint(name="To Group")
db = AsyncDatabase.get_current()
symbols = {0: "🌝", 1: "🌚"}


async def create_dialog(obj: dict) -> list:
    if not obj["fwd_messages"]:
        return []

    fwd: List[dict] = obj["fwd_messages"]
    users = await get_name(get_users(obj))
    return [
        "{} [id{}|{}]: {}".format(
            symbols[fwd.index(i) % 2 == 0],
            i["from_id"], users[i["from_id"]],
            i["text"]
        )
        for i in obj["fwd_messages"]
    ]


@bot.event.to_group()
async def wrapper(event: ToGroup):
    peer_id = db.chats(event.object.chat)
    data = await get_by_local(peer_id, event.object.local_id)
    from_id = event.message.from_id
    if "reply_message" not in data:
        attachments = get_attachments(data)
        message = []
    else:
        attachments = get_attachments(data["reply_message"])
        message = [data["reply_message"]["text"]]
        from_id = data["reply_message"]["from_id"]

    if "диалог" in event.message.text:
        message.extend(await create_dialog(data))

    if "автор" in event.message.text:
        message.append("\n\n🗣 Автор: [id{}|{}]".format(
            from_id, await get_name(from_id)
        ))

    if not any([message, attachments]):
        return await send_msg(peer_id, "❗ Запись не может быть пустой.")

    await bot.api.wall.post(
        owner_id=-event.object.group_id,
        from_group=True,
        attachments=attachments,
        message="\n".join(message).replace("!вгр", ""),
        guid=0
    )
    return await send_msg(peer_id, "✅ Запись опубликована!")