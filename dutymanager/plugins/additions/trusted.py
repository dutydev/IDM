from dutymanager.units.utils import get_by_local, get_name
from dutymanager.db.methods import AsyncDatabase, Trusted
from dutymanager.units.vk_script import msg_edit
from dutymanager.units.utils import get_users
from module.objects.types import SendMySignal
from module import Blueprint, Method

bot = Blueprint(name="Trusted")
db = AsyncDatabase.get_current()
patterns = [
    "+дов", "-дов",
    "+доверенный", "-доверенный"
]

ADDED = "✅ Пользователи ({}) добавлены в список доверенных."
REMOVED = "✅ Пользователи ({}) убраны из списка доверенных."


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=["довы", "доверенные"],
    lower=True
)
async def get_trusted(event: SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    message = [
        f"✅ Доверенный: [id{k}|{v}]"
        for k, v in db.trusted.items()
    ]
    if not message:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Список пуст."
        )
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="\n".join(message)
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=patterns,
    lower=True
)
async def add_trusted(event: SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    users = get_users(await get_by_local(peer_id, local_id))
    if not users:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Ошибка, перешлите сообщение."
        )
    if "-дов" in event.object.value:
        return await remove_trusted(event, users)
    count = await db.trusted.create_many([
        Trusted(uid=k, name=v)
        for k, v in (await get_name(users)).items()
        if k not in db.trusted
    ])
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message=ADDED.format(count)
    )


async def remove_trusted(
    event: SendMySignal, users: list
):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    count = await db.trusted.remove_many([
        i for i in users if i in db.trusted
    ])
    return await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message=REMOVED.format(count)
    )
