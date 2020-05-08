from dutymanager.db.methods import AsyncDatabase
from dutymanager.files.errors import VK_ERROR
from dutymanager.units.utils import *
from module import VKError, types
from module import Blueprint

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.event.ban_expired()
async def ban_expired(event: types.BanExpired):
    peer_id = db.chats(event.object.chat)
    user_id = event.object.user_id
    try:
        await bot.api.messages.add_chat_user(
            chat_id=int(peer_id - 2e9),
            user_id=user_id
        )
    except VKError as e:
        error = list(e.args)[0]
        await send_msg(
            peer_id=int(peer_id - 2e9),
            message=f"⚠ Произошла ошибка на этапе добавления забаненого [id{user_id}|пользователя]."
                    f"\nВК ответил: {error[1]} ({error[0]})"
                    f"\nПричина бана: {event.object.comment[:250]}"
        )


@bot.event.add_user()
async def add_user(event: types.AddUser):
    peer_id = db.chats(event.object.chat)
    user_id = event.object.user_id
    try:
        await bot.api.messages.add_chat_user(
            chat_id=int(peer_id - 2e9),
            user_id=user_id
        )
    except VKError as e:
        e = list(e.args)
        await send_msg(
            peer_id=peer_id,
            message=f"⚠ Произошла ошибка на этапе добавления [id{user_id}|пользователя]."
                    f"\nВК ответил: {VK_ERROR.get(e[0])}"
        )
