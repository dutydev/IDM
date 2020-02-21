from ...objects import dp, SignalEvent
from ...utils import new_message

@dp.signal_event_handle('повтори')
def repiat(event: SignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message=event.payload,
        attachments=",".join(event.attachments))

    return "ok"
