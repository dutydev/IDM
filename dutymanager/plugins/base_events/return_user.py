from module import Blueprint, Method
from module import VKError, types
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import *

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.on.event(Method.BAN_EXPIRED)
async def ban_expired(event: types.BanExpired):
    uid = event.object.chat
    user_id = event.object.user_id
    try:
        await bot.api.messages.add_chat_user(
            chat_id=int(db.chats[uid] - 2e9),
            user_id=user_id
        )
    except VKError as e:
        error = list(e.args)[0]
        await send_msg(
            peer_id=int(db.chats[uid] - 2e9),
            message=f"⚠ Произошла ошибка на этапе добавления забаненого [id{user_id}|пользователя]."
                    f"\nВК ответил: {error[1]} ({error[0]})"
                    f"\nПричина бана: {event.object.comment[:250]}"
        )


@bot.on.event(Method.ADD_USER)
async def add_user(event: types.AddUser):
    uid = event.object.chat
    user_id = event.object.user_id
    try:
        await bot.api.messages.add_chat_user(
            chat_id=int(db.chats[uid] - 2e9),
            user_id=user_id
        )
    except VKError as e:
        e = list(e.args)[0]
        await send_msg(
            peer_id=db.chats[uid],
            message=f"⚠ Произошла ошибка на этапе добавления [id{user_id}|пользователя]."
                    f"\nВК ответил: {e[1]} ({e[0]})"
        )
