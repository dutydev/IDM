from module import Blueprint, Method
from module import types
from dutymanager.core.config import ping_state
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.vk_script import msg_edit
from time import time as current
from datetime import datetime


bot = Blueprint()
db = AsyncDatabase.get_current()
responses = {
    'пинг': 'понг',
    'кинг': 'конг',
    'пиф': 'паф',
    'пиу': 'пау'
}


async def abstract_ping(
        uid: str, text: str,
        timestamp: int, local_id: int
):
    message = ping_state.format(
        "",
        responses[text].upper(),
        round(current() - timestamp, 2),
        datetime.fromtimestamp(timestamp),
        datetime.fromtimestamp(int(current()))
    )
    await msg_edit(db.chats[uid], message, local_id)


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    list(responses.keys()),
    lower=True
)
async def send_my_signal(event: types.SendMySignal):
    await abstract_ping(
        event.object.chat,
        event.object.value,
        event.message.date,
        event.object.conversation_message_id
    )


@bot.event.message_signal(
    Method.SEND_SIGNAL,
    list(responses.keys()),
    lower=True
)
async def send_signal(event: types.SendSignal):
    if event.object.from_id in db.trusted:
        await abstract_ping(
            event.object.chat,
            event.object.value,
            event.message.date,
            event.object.conversation_message_id
        )