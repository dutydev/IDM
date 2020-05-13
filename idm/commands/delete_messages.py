from ..objects import dp, Event
from .. import utils
from vkapi import VkApiResponseException
import time

@dp.event_handle(dp.Methods.DELETE_MESSAGES)
def delete_messages(event: Event) -> str:
    message_id = utils.new_message(event.api, event.chat.peer_id, message="УДАЛЯЮ ПАДАЖЖЫ")
    msg_ids = utils.get_msg_ids(event.api, event.chat.peer_id, event.obj['local_ids'])
    if msg_ids == None or msg_ids == []:
        utils.edit_message(event.api, event.chat.peer_id, message_id, message="❗ Ошибка, не нашел мессаги 🤷‍♀")
        return "ok"
    msgs = event.api('messages.getHistory', peer_id = event.chat.peer_id)['items']
    for i in range(20):
        if (msgs[i])['text'] == '-смс':
            utils.delete_message(event.api, event.chat.peer_id, (msgs[i])['id'])
    msg_ids = [str(msg_id) for msg_id in msg_ids]
    try:
        event.api("messages.delete", message_ids=",".join(msg_ids), delete_for_all=1, spam=1 if event.obj.get("is_spam", False) else 0)
        utils.edit_message(event.api, event.chat.peer_id, message_id, message="✅ Удалено (3)")
        time.sleep(1)
        utils.edit_message(event.api, event.chat.peer_id, message_id, message="✅ Удалено (2)")
        time.sleep(1)
        utils.edit_message(event.api, event.chat.peer_id, message_id, message="✅ Удалено (1)")
        time.sleep(1)
        utils.delete_message(event.api, event.chat.peer_id, message_id)
    except VkApiResponseException as e:
        if e.error_code == 924:
            utils.edit_message(event.api, event.chat.peer_id, message_id, message="❗ Не прокатило. Пользователь администратор? 🤔")
        else:
            utils.edit_message(event.api, event.chat.peer_id, message_id, message=f"❗ Не прокатило. Ошибка VK {e.error_msg}")
    except:
        utils.edit_message(event.api, event.chat.peer_id, message_id, message=f"❗ Мутота какая-то случилась, хз.")
    return "ok"