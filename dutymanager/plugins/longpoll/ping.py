from ..additions.ping import responses, patterns
from dutymanager.files.msgs import ping_state
from module import Blueprint, Message
from time import time as current
from datetime import datetime

bot = Blueprint(name="LongPoll")


@bot.on.chat_message(text=patterns, lower=True)
async def wrapper(ans: Message):
    text = ans.text.lower().split()
    timestamp = ans.date
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
    await bot.api.messages.edit(
        peer_id=ans.peer_id,
        message_id=ans.message_id,
        message=message
    )