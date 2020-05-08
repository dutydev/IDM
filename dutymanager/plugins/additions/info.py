from dutymanager.db.methods import AsyncDatabase
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Information")
db = AsyncDatabase.get_current()
patterns = ["инфо", "инфа", "-i", "info"]


async def abstract_info(uid: str, local_id: str, method: str):
    pass


@bot.event.message_signal(
    Method.SEND_SIGNAL,
    text=patterns,
    lower=True
)
async def send_signal(event: types.SendSignal):
    pass


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=patterns,
    lower=True
)
async def send_my_signal(event: types.SendMySignal):
    pass
