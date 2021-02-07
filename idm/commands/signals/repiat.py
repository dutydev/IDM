from ...objects import dp, SignalEvent
from ...utils import new_message


@dp.signal_event_handle('повтори')
def repiat(event: SignalEvent) -> str:
    if event.msg['from_id'] not in event.db.trusted_users:
        return "ok"
    new_message(event.api, event.chat.peer_id, message=event.payload,
                attachments=",".join(event.attachments))

    return "ok"
