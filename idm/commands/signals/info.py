from ...objects import dp, MySignalEvent, SignalEvent, __version__
from ...utils import edit_message, new_message, delete_message, ment_user
from datetime import datetime
import time

@dp.signal_event_register('инфо', 'инфа', 'info')
def sinfo(event: SignalEvent) -> str:
    if event.msg['from_id'] not in event.db.trusted_users:
        message_id = new_message(event.api, event.chat.peer_id,
        message = event.responses['not_in_trusted'])
        time.sleep(3)
        delete_message(event.api, event.chat.peer_id, message_id)
        return "ok"

    owner = event.api('users.get', user_ids=event.db.duty_id)[0]

    new_message(event.api, event.chat.peer_id, message = event.responses['info_duty'].format(
    версия = __version__, владелец = ment_user(owner), чаты = len(event.db.chats.keys()),
    ид = event.chat.iris_id, имя = event.chat.name))

    return "ok"