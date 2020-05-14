from dutymanager.units.vk_script import generate_history
from dutymanager.units.utils import send_msg
from dutymanager.db.methods import AsyncDatabase
from module.objects.types import SendMySignal
from module import Blueprint, Method
from time import time

bot = Blueprint(name="Delete self messages")
db = AsyncDatabase.get_current()


async def delete_messages(ids: list):
    code = """var ids = %s;
    var a = 0;
    while (a < ids.length) {
        API.messages.delete({
            "message_ids": ids.slice(a, a + 500),
            "delete_for_all": 1
        });
        a = a + 500;
    }"""
    for i in range(0, len(ids), 12500):
        await bot.api.execute(code % ids[i: i + 12500])


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="-смс <num:int>"
)
async def delete_by_count(event: SendMySignal, num: int):
    peer_id = db.chats(event.object.chat)
    history = await generate_history(
        peer_id=peer_id,
        offset_max=(200, 5000)[num >= 200]
    )
    await delete_messages([
        i["id"] for i in history if i["from_id"] == bot.user_id
        and "action" not in i
        and time() - i["date"] < 86400
    ])
    await send_msg(peer_id, "Сообщения удалены.")


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="-смс за <unix:unix>"
)
async def delete_by_time(event: SendMySignal, unix: int):
    pass