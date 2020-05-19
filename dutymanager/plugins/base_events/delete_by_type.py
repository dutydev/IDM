from dutymanager.units.vk_script import (
    generate_history, delete_messages
)
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import send_msg
from module import Blueprint
from module import types
from time import time

bot = Blueprint()
db = AsyncDatabase.get_current()
clipboard = dict(
    wall="wall", photo="photo",
    stickers="sticker", gif="gif",
    voice="audio_message",
    video="video", audio="audio",
    forwarded="forwarded",
    article="article"
)
words = dict(
    wall="с репостами",
    photo="с изображениями",
    sticker="со стикерами",
    audio_message="с голосовыми",
    gif="с гифками",
    video="с видеороликами",
    audio="с аудиозаписями"
)


@bot.event.delete_messages_by_type()
async def delete_by_type(event: types.DeleteMessagesByType):
    peer_id = db.chats(event.object.chat)
    kind = clipboard[event.object.type]
    offset = event.object.offset
    message_ids = []
    for i in await generate_history(
        peer_id=peer_id, offset_min=offset,
        start_message_id=event.object.local_id
    ):
        if (time() - i["date"]) > 86400:
            continue

        if kind == "forwarded":
            if i["fwd_messages"] or i.get("reply_message"):
                message_ids.append(i["id"])

        else:
            attachments = i["attachments"] or [{"type": "1"}]
            if any([i["type"] == kind for i in attachments]):
                message_ids.append(i["id"])

    if not message_ids:
        return await send_msg(
            peer_id, "❎ Сообщения {} не найдены.".format(
                words.get(kind, '')
            )
        )

    await delete_messages(message_ids, event.object.is_spam)
    return await send_msg(
        peer_id, f"✅ Сообщения {words.get(kind, '')} удалены."
    )