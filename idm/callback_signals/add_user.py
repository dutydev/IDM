from idm.objects import dp, Event
from idm.utils import ment_user
from microvk import VkApiResponseException
import json

def user_add(event: Event, typ: str):
    user = event.api('users.get', user_ids=event.obj['user_id'])[0]
    message_id = event.api.msg_op(1, event.chat.peer_id,
        event.responses[typ].format(ссылка = ment_user(user), имя = event.chat.name))

    try: # не надо вот тут, чел просто попросил, я по-быстренькому сделал, все довольны, на код всем похуй
        event.api('messages.removeChatUser', chat_id=event.chat.id, user_id=user['id'])
    except VkApiResponseException:
        pass

    try:
        event.api('messages.addChatUser', chat_id=event.chat.id, user_id=user['id'])
        message = event.responses['user_ret_success'].format(ссылка = 
        ment_user(user), имя = event.chat.name)
        ret = "ok"
    except VkApiResponseException as e:
        if e.error_code == 15:
            message = event.responses['user_ret_err_no_access'].format(ссылка = 
            ment_user(user), имя = event.chat.name)
        else:
            message = (event.responses['user_ret_err_vk'].format(ссылка = 
            ment_user(user), имя = event.chat.name, ошибка = e.error_msg))
        ret = {"response":"vk_error",
        "error_code": e.error_code,"error_message": e.error_msg}
    except:
        message = event.responses['user_ret_err_unknown'].format(ссылка = 
        ment_user(user), имя = event.chat.name)
        ret = {"response":"error","error_code":"0","error_message":""}

    event.api.msg_op(2, event.chat.peer_id, message, message_id)
    return ret


@dp.event_register('addUser')
def add_user(event: Event) -> str:
    return user_add(event, 'user_ret_process')


@dp.event_register('banExpired')
def ban_expired(event: Event) -> str:
    return user_add(event, 'user_ret_ban_expired')
