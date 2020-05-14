from dutymanager.units.utils import get_users, get_by_local
from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from module.objects.types import SendMySignal
from module import Blueprint, Method

bot = Blueprint(name="Friends add")
db = AsyncDatabase.get_current()


async def friends_request(ids: list, add: bool) -> int:
    method = (
        'API.friends.add({"user_id": ids[a], "follow": 0});'
        if add else
        'API.friends.delete({"user_id": ids[a]});'
    )
    code = """var ids = %s;
    var a = 0;
    while (a < ids.length) {
        %s
        a = a + 1;
    }
    return 1;"""
    for i in range(0, len(ids), 25):
        await bot.api.execute(code % (ids[i: i + 25], method))
    return len(ids)


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=["+др", "-др"]
)
async def add_friends(event: SendMySignal):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    users = get_users(await get_by_local(peer_id, local_id))
    if not users:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Ошибка, перешлите сообщение."
        )
    if "-др" in event.object.value:
        return await remove_friends(event, users)
    count = await friends_request(
        ids=[
            i.user_id
            for i in await bot.api.friends.are_friends(user_ids=users)
            if i.friend_status in (0, 2)
        ],
        add=True
    )
    await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message=f"✅ Отправлено ({count}) заявок."
    )


async def remove_friends(event: SendMySignal, users: list):
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    count = await friends_request(
        ids=[
            i.user_id
            for i in await bot.api.friends.are_friends(user_ids=users)
            if i.friend_status in (1, 3)
        ],
        add=False
    )
    await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message=f"✅ Удалено {count}."
    )