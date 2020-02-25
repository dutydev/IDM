from ..objects import dp, Event
from .. import utils
from vkapi import VkApiResponseException
from datetime import datetime

@dp.event_handle(dp.Methods.DELETE_MESSAGES_FROM_USER)
def delete_messages_from_user(event: Event) -> str:
    message_id = utils.new_message(event.api, event.chat.peer_id, message="... удаляю сообщения ...")

    user_id = event.obj['user_id']
    amount = event.obj.get("amount", None)

    msg_ids = []
    for mmsg in utils.get_all_history_gen(event.api, event.chat.peer_id):
        if datetime.now().timestamp() - mmsg['date'] >= 86400:
            break        
        if mmsg['from_id'] == user_id and mmsg.get('action', None) == None:
            msg_ids.append(str(mmsg['id']))

    if amount != None:
        if amount <= len(msg_ids):            
            msg_ids = msg_ids[:len(msg_ids) - (len(msg_ids) - amount)]

    try:
        event.api("messages.delete", message_ids=",".join(msg_ids), delete_for_all=1, spam=1 if event.obj.get("is_spam", False) else 0)        
        utils.edit_message(event.api, event.chat.peer_id, message_id, message="✅ Сообщения удалены")
    except VkApiResponseException as e:
        if e.error_code == 924:
            utils.edit_message(event.api, event.chat.peer_id, message_id, message="❗ Не удалось удалить сообщения. Невозможно удалить сообщение, возможно пользователь администратор.")
        else:
            utils.edit_message(event.api, event.chat.peer_id, message_id, message=f"❗ Не удалось удалить сообщения. Ошибка VK {e.error_msg}")
    except:
        utils.edit_message(event.api, event.chat.peer_id, message_id, message=f"❗ Произошла неизвестная ошибка.")
    return "ok"