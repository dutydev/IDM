from module.objects.types import SendMySignal, SendSignal
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.vk_script import msg_edit
from dutymanager.files.msgs import ping_state
from module import Blueprint, Method
from datetime import datetime
from typing import List
from time import time

bot = Blueprint()
db = AsyncDatabase.get_current()
responses = {
    'пинг': 'ПОНГ',
    'кинг': 'КОНГ',
    'пиф': 'ПАФ',
    'пиу': 'ПАУ'
}
patterns = [
    "пинг", "пинг %debug",
    "кинг", "кинг %debug",
    "пиу", "пиу %debug",
    "пиф", "пиф %debug"
]
average: List[float] = []


async def abstract_ping(
    uid: str, text: str,
    timestamp: int, local_id: int
):
    text = text.split()
    current = round(time() - timestamp, 2)
    average.append(current)
    if text[-1] == "%debug":
        message = ping_state.format(
            responses[text[0]], current,
            round(sum(average) / len(ping_state), 2),
            datetime.fromtimestamp(timestamp),
            datetime.fromtimestamp(int(time()))
        )
    else:
        message = "{}\nОтвет через: {} сек.".format(
            responses[text[0]], current
        )
    await msg_edit(db.chats(uid), message, local_id)


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    patterns,
    lower=True
)
async def send_my_signal(event: SendMySignal):
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
async def send_signal(event: SendSignal):
    if event.object.from_id in db.trusted:
        await abstract_ping(
            event.object.chat,
            event.object.value,
            event.message.date,
            event.object.conversation_message_id
        )