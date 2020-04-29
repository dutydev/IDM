from module import Blueprint, Message
from ..additions.ping import responses

bot = Blueprint(name="LongPoll")
patterns = ["!л пинг"]


@bot.on.chat_message(text="!л пинг")
async def wrapper(ans: Message):
    await ans("Test")