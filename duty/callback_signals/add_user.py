from duty.objects import dp, Event
from duty.utils import ment_user, format_response
from microvk import VkApiResponseException


def user_add(event: Event, typ: str):
    user = event.api('users.get', user_ids=event.obj['user_id'])[0]


    def _format(response_name, err=None):
        return format_response(
            event.responses[response_name],
            ссылка=ment_user(user), имя=event.chat.name, ошибка=err
        )

    if event.obj['user_id'] == event.db.owner_id:
        event.send(_format('user_ret_self'))

        return 'ok'

    message_id = event.send(_format(typ))

    try:
        event.api('messages.removeChatUser',
                  chat_id=event.chat.id, user_id=user['id'])
    except VkApiResponseException:
        pass

    try:
        event.api('messages.addChatUser',
                  chat_id=event.chat.id, user_id=user['id'])
        event.edit_msg(message_id, _format('user_ret_success'))
        return "ok"
    except VkApiResponseException as e:
        if e.error_code == 15:
            event.edit_msg(message_id, _format('user_ret_err_no_access'))
        else:
            event.edit_msg(message_id, _format('user_ret_err_vk', e.error_msg))
        return {
            "response":"vk_error",
            "error_code": e.error_code,
            "error_message": e.error_msg
        }
    except Exception:
        event.edit_msg(message_id, _format('user_ret_err_unknown'))
        return {"response":"error","error_code":"0","error_message":""}


@dp.event_register('addUser')
def add_user(event: Event) -> str:
    return user_add(event, 'user_ret_process')


@dp.event_register('banExpired')
def ban_expired(event: Event) -> str:
    return user_add(event, 'user_ret_ban_expired')
