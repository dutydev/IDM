from module import Blueprint, Message
from ..additions.ping import responses
from dutymanager.files.msgs import ping_state
from time import time as current
from datetime import datetime

bot = Blueprint(name="LongPoll")


@bot.on.chat_message(text=list(responses.keys()), lower=True)
async def wrapper(ans: Message):
    if bot.user_id == ans.from_id:
        await bot.api.messages.edit(
            peer_id=ans.peer_id,
            message_id=ans.message_id,
            message=ping_state.format(
                "[User LP]",
                responses[ans.text.lower()].upper(),
                round(current() - ans.date, 2),
                datetime.fromtimestamp(ans.date),
                datetime.fromtimestamp(int(current()))
            )
        )