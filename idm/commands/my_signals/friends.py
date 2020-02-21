from ...objects import dp, MySignalEvent
from ...utils import new_message, edit_message
from vkapi import VkApiResponseException

@dp.my_signal_event_handle('+др', '+друг')
def add_to_fr(event: MySignalEvent) -> str:
    if event.reply_message == None:
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Ошибка при выполнении, необходимо пересланное сообщение")
        return "ok"

    friend_id = event.reply_message['from_id']
    try:
        event.api('friends.add', user_id=friend_id)
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
            message="✅ Все отлично, запрос отправлен")
        return "ok"
    except VkApiResponseException as e:
        if e.error_code == 174:
            edit_message(event.api, event.chat.peer_id, event.msg['id'],
            message="❗ Невозможно добавить в друзья самого себя")
        elif e.error_code == 175:
            edit_message(event.api, event.chat.peer_id, event.msg['id'],
                message="❗ Невозможно добавить в друзья пользователя, который занес Вас в свой черный список")
        elif e.error_code == 176:
            edit_message(event.api, event.chat.peer_id, event.msg['id'],
                message="❗ Невозможно добавить в друзья пользователя, который занесен в Ваш черный список")
        else:
            edit_message(event.api, event.chat.peer_id, event.msg['id'],
                message=f"❗ Невозможно добавить в друзья пользователя: {e.error_msg}")
        return "ok"

@dp.my_signal_event_handle('-др', '-друг')
def remove_from_fr(event: MySignalEvent) -> str:
    if event.reply_message == None:
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
                message="❗ Ошибка при выполнении, нужно пересланное сообщение")
        return "ok"

    friend_id = event.reply_message['from_id']
    
    try:
        data = event.api('friends.delete', user_id=friend_id)
        if data.get('friend_deleted', False):edit_message(event.api, event.chat.peer_id, event.msg['id'], message="✅ Друг удален")
        elif data.get('out_request_deleted', False):edit_message(event.api, event.chat.peer_id, event.msg['id'], message="✅ Отменена исходящая заявка")
        elif data.get('in_request_deleted', False):edit_message(event.api, event.chat.peer_id, event.msg['id'], message="✅ Отклонена входящая заявка")
        elif data.get('suggestion_deleted', False):edit_message(event.api, event.chat.peer_id, event.msg['id'], message="✅ Отклонена рекомендация друга")
        elif data.get('success', False):edit_message(event.api, event.chat.peer_id, event.msg['id'], message="✅ Друг удален")
        else:edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Произошла ошибка")
    except VkApiResponseException as e:
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"❗ Произошла ошибка VK №{e.error_code} {e.error_msg}")
    


    return "ok"
