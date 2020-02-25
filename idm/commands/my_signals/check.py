from ...objects import dp, MySignalEvent
from ... import utils
from vkapi import VkApi

@dp.my_signal_event_handle('проверить')
def check(event: MySignalEvent) -> str:
    def check_token(t: str) -> str:

        if t == "" or t == None:
            return "Токен не задан"

        api = VkApi(t)

        user = api('users.get')

        if type(user) != list:
            return "ошибка | токен поврежден"
        user = user[0]

        return f"ОК, [id{user['id']}|{user['first_name']} {user['last_name']}]"
    

    message = f"""
    Основной токен: {check_token(event.db.access_token)}
    Токен для вечного онлайна: {check_token(event.db.online_token)}
    Токен для скрытия онлайна: {check_token(event.db.me_token)}
    Токен для добавления групп: {check_token(event.db.bp_token)}
    
    """.replace('    ', '')

    utils.new_message(event.api, event.chat.peer_id, message=message)
    





    return "ok"

