from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.vk_script import msg_edit
from dutymanager.files.msgs import ping_state
from module import Blueprint, Method
from time import time as current
from datetime import datetime
from module import types

bot = Blueprint()
db = AsyncDatabase.get_current()
responses = {
    'пинг': 'понг',
    'кинг': 'конг',
    'пиф': 'паф',
    'пиу': 'пау'
}
patterns = [
    "пинг", "пинг %time",
    "кинг", "кинг %time",
    "пиу", "пиу %time",
    "пиф", "пиф %time"
]


async def abstract_ping(
    uid: str, text: str,
    timestamp: int, local_id: int
):
    text = text.split()
    if text[-1] == "%time":
        message = ping_state.format(
            responses[text[0]].upper(),
            round(current() - timestamp, 2),
            datetime.fromtimestamp(timestamp),
            datetime.fromtimestamp(int(current()))
        )
    else:
        message = "{}\nОтвет через: {} сек.".format(
            responses[text[0]].upper(),
            round(current() - timestamp, 2)
        )
    await msg_edit(db.chats(uid), message, local_id)


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    patterns,
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
    patterns,
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