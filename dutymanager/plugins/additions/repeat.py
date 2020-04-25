from module import Blueprint, Method
from module import types
from dutymanager.units.utils import *
from dutymanager.db.methods import AsyncDatabase


bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.on.message_event(Method.SEND_SIGNAL, text="повтори <text>")
async def repeat(event: types.SendSignal, text: str):
    peer_id = db.chats[event.object.chat]
    if event.object.from_id in db.trusted:
        attachments = await get_attachments(await get_by_local(
            peer_id, event.object.conversation_message_id
        ))
        await send_msg(peer_id, f"{text}", attachment=attachments)