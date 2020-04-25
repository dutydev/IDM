from module import Blueprint, Method
from module import types
from dutymanager.units.utils import *
from dutymanager.core.config import ping_state
from dutymanager.db.methods import AsyncDatabase
from time import time as current


bot = Blueprint()
db = AsyncDatabase.get_current()
responses = {
    'пинг': 'понг',
    'кинг': 'конг',
    'пиф': 'паф',
    'пиу': 'пау'
}


async def abstract_ping(uid: str, text: str, timestamp: int):
    await send_msg(
        peer_id=db.chats[uid],
        message=ping_state.format(
            responses[text].title(),
            round(current() - timestamp, 2)
        )
    )


@bot.on.message_event(
    Method.SEND_MY_SIGNAL,
    list(responses.keys()),
    lower=True
)
async def send_my_signal(event: types.SendMySignal):
    await abstract_ping(
        event.object.chat,
        event.object.value,
        event.message.date
    )


@bot.on.message_event(
    Method.SEND_SIGNAL,
    list(responses.keys()),
    lower=True
)
async def send_signal(event: types.SendSignal):
    if event.object.from_id in db.trusted:
        await abstract_ping(
            event.object.chat,
            event.object.value,
            event.message.date
        )