
from ..objects import dp, Event
from .. import utils
from vkapi import VkApiResponseException

@dp.event_handle(dp.Methods.FORBIDDEN_LINKS)
def forbidden_links(event: Event) -> str:
    message_id = utils.new_message(event.api, event.chat.peer_id, message="... удаляю сообщения ...")

    msg_ids = utils.get_msg_ids(event.api, event.chat.peer_id, event.obj['local_ids'])
    msg_ids = [str(msg_id) for msg_id in msg_ids]

    if msg_ids == None or msg_ids == []:
        utils.edit_message(event.api, event.chat.peer_id, message_id, message="❗ Ошибка дежурного, я не смог найти смс")
        return "ok"

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