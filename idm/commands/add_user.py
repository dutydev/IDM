from ..objects import dp, Event
from ..utils import new_message, edit_message, user_f
from microvk import VkApiResponseException
import json

def user_add(event, typ):
    user = event.api('users.get', user_ids=event.obj['user_id'])[0]
    message_id = new_message(event.api, event.chat.peer_id,
    message = event.responses[typ].format(ссылка = user_f(user), имя = event.chat.name))
    try:
        event.api('messages.addChatUser', chat_id=event.chat.id, user_id=user['id'])
        message = event.responses['user_ret_success'].format(ссылка = 
        user_f(user), имя = event.chat.name)
        ret = "ok"
    except VkApiResponseException as e:
        if e.error_code == 15:
            message = event.responses['user_ret_err_no_access'].format(ссылка = 
            user_f(user), имя = event.chat.name)
        else:
            message = (event.responses['user_ret_err_vk'].format(ссылка = 
            user_f(user), имя = event.chat.name, ошибка = e.error_msg))
        ret = {"response":"vk_error",
        "error_code": e.error_code,"error_message": e.error_msg}
    except:
        message = event.responses['user_ret_err_unknown'].format(ссылка = 
        user_f(user), имя = event.chat.name)
        ret = {"response":"error","error_code":"0","error_message":""}

    edit_message(event.api, event.chat.peer_id, message_id, message=message)
    return ret

@dp.event_handle('addUser')
def add_user(event: Event) -> str:
    return user_add(event, 'user_ret_process')

@dp.event_handle('banExpired')
def ban_expired(event: Event) -> str:
    return user_add(event, 'user_ret_ban_expired')