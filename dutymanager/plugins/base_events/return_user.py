from module.objects.types import BanExpired, AddUser
from dutymanager.db.methods import AsyncDatabase
from module import Blueprint

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.event.ban_expired()
async def ban_expired(event: BanExpired):
    peer_id = db.chats(event.object.chat)
    user_id = event.object.user_id
    await bot.api.messages.add_chat_user(
        chat_id=int(peer_id - 2e9),
        user_id=user_id
    )


@bot.event.add_user()
async def add_user(event: AddUser):
    peer_id = db.chats(event.object.chat)
    user_id = event.object.user_id
    await bot.api.messages.add_chat_user(
        chat_id=int(peer_id - 2e9),
        user_id=user_id
    )
