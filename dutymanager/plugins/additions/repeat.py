from dutymanager.db.methods import AsyncDatabase
from module import Blueprint, Method
from dutymanager.units.utils import *
from module import types

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.event.message_signal(Method.SEND_SIGNAL, text="повтори <text>")
async def repeat(event: types.SendSignal, text: str):
    peer_id = db.chats(event.object.chat)
    from_id = event.object.from_id
    if from_id in (*db.trusted.keys(), bot.user_id):
        attachments = await get_attachments(await get_by_local(
            peer_id, event.object.conversation_message_id
        ))
        await send_msg(peer_id, f"{text}", attachment=attachments)