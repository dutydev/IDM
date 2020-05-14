from module import Blueprint, Message
from vkbottle.ext import Middleware

bot = Blueprint(name="Middleware")


@bot.middleware.middleware_handler()
class Discourage(Middleware):
    async def middleware(self, ans: Message):
        if ans.from_id != bot.user_id:
            return False
