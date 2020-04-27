from module import Blueprint, Message

bot = Blueprint(name="LongPoll")


@bot.on.chat_message(text="!test")
async def wrapper(ans: Message):
    await ans("Test")