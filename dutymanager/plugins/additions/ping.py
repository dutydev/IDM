from datetime import datetime
from time import time
from dutymanager.units.tools import get_case
from dutymanager.db.methods import AsyncDatabase
from dutymanager.files.msgs import ping_state
from dutymanager.units.vk_script import msg_edit
from module import Blueprint, Method
from module.objects.types import SendMySignal, SendSignal

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


async def abstract_ping(
    uid: str, text: str,
    timestamp: int, local_id: int
):
    text = text.split()
    current = round(time() - timestamp, 2)
    if text[-1] == "%debug":
        message = ping_state.format(
            responses[text[0]], current,
            datetime.fromtimestamp(timestamp),
            datetime.fromtimestamp(int(time()))
        )
    else:
        message = "{}\nОтвет через: {}".format(
            responses[text[0]],
            get_case(current, 'секунда')
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