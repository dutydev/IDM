from ...objects import dp, SignalEvent
from ...utils import new_message, delete_message
import time

@dp.signal_event_register('повтори', 'скажи', 'напиши')
def repeat(event: SignalEvent) -> str:
    if event.msg['from_id'] not in event.db.trusted_users:
        message_id = new_message(event.api, event.chat.peer_id,
        message = event.responses['not_in_trusted'])
        time.sleep(3)
        delete_message(event.api, event.chat.peer_id, message_id)
        return "ok"

    msg = event.payload.lower()
    for word in event.responses['repeat_forbidden_words']:
        if word in msg or msg.startswith('!'):
            new_message(event.api, event.chat.peer_id,
            message= event.responses['repeat_if_forbidden'])
            return "ok"

    new_message(event.api, event.chat.peer_id, message=event.payload,
        attachments=",".join(event.attachments))
    return "ok"
