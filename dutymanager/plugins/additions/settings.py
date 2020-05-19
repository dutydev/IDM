from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.vk_script import msg_edit
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Settings")
db = AsyncDatabase.get_current()


async def set_limit(limit: int, uid: str, local_id: int):
    peer_id = db.chats(uid)
    if limit <= 0:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Лимит должен быть не меньше 0."
        )
    db.settings.change(page_limit=limit)
    db.create_pages(limit)
    await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="✅ Лимит шаблонов на одной странице был изменён."
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="лимит <page:int>",
    lower=True
)
async def send_my_signal(event: types.SendMySignal, page: int):
    await set_limit(
        page, event.object.chat,
        event.message.conversation_message_id
    )


@bot.event.message_signal(
    Method.SEND_SIGNAL,
    text="лимит <page:int>",
    lower=True
)
async def send_signal(event: types.SendSignal, page: int):
    if event.object.from_id in db.trusted:
        await set_limit(
            page, event.object.chat,
            event.message.conversation_message_id
        )