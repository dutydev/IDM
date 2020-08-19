# да-да, я знаю про повтор кода, отстань
from .utils import msg_op, parseByID, find_mention_by_message, parse
from microvk import VkApiResponseException
from . import dlp


@dlp.register_startswith('+др', '+друг', '-др', '-друг')
def change_friend_status(nd) -> str:
    msg = nd.msg
    user_id = find_mention_by_message(msg, nd.vk)
    if user_id:
        if msg['command'].startswith('-др'):
            try:
                status = nd.vk('friends.delete', user_id = user_id)
                if status.get('friend_deleted'): msg = "💔 Пользователь удален из друзей"
                elif status.get('out_request_deleted'): msg = "✅ Отменена исходящая заявка"
                elif status.get('in_request_deleted'): msg = "✅ Отклонена входящая заявка"
                elif status.get('suggestion_deleted'): msg = "✅ Отклонена рекомендация друга"
                else: msg = "❗ Произошла ошибка"
            except VkApiResponseException as e:
                msg = f"❗ Произошла ошибка VK №{e.error_code} {e.error_msg}"
        else:
            try:
                status = nd.vk('friends.add', user_id = user_id)
                if status == 1: msg = "✅ Заявка отправлена"
                elif status == 2: msg = "✅ Заявка принята"
                else: msg = "✅ Заявка отправлена повторно"
            except VkApiResponseException as e:
                if e.error_code == 174:
                    msg = "🤔 Ты себя добавить хочешь?"
                elif e.error_code == 175:
                    msg = "❗ Ты в ЧС данного пользователя"
                elif e.error_code == 176:
                    msg = "❗ Пользователь в ЧС"
                else:
                    msg = f"❗ Ошибка: {e.error_msg}"
    else:
        msg = "❗ Необходимо пересланное сообщение или упоминание"
    msg_op(2, nd[3], msg, nd[1])
    return "ok"
    

@dlp.register_startswith('+чс', '-чс')
def ban_user(nd):
    msg = nd.msg
    user_id = find_mention_by_message(msg, nd.vk)
    if user_id:
        if msg['command'] == '+чс':
            try:
                if nd.vk('account.ban', owner_id = user_id) == 1:
                    msg = '😡 Забанено'
            except VkApiResponseException as e:
                if e.error_msg.endswith('already blacklisted'):
                    msg = '❗ Пользователь уже забанен'
                else: msg = f'❗ Ошиб_очка: {e.error_msg}'
        else:
            try:
                if nd.vk('account.unban', owner_id = user_id) == 1:
                    msg = '💚 Разбанено'
            except VkApiResponseException as e:
                if e.error_msg.endswith('not blacklisted'):
                    msg = '👌🏻 Пользователь не забанен'
                else: msg = f'❗ Ошиб_очка: {e.error_msg}'
    else:
        msg = "❗ Необходимо пересланное сообщение или упоминание"
    msg_op(2, nd[3], msg, nd[1], delete = 1)
    return "ok"