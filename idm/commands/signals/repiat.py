from ...objects import dp, SignalEvent
from ...utils import new_message

@dp.signal_event_handle('повтори', 'скажи', 'с')
def repeat(event: SignalEvent) -> str:
    if event.msg['from_id'] not in event.db.trusted_users:
        return "ok"
    if ('передать' in event.payload.lower() or 'повысить' in event.payload.lower()
	or 'модер' in event.payload.lower() or 'завещание' in event.payload.lower()):
        new_message(event.api, event.chat.peer_id,
        message= 'Я это писать не буду.')
        return "ok"
    new_message(event.api, event.chat.peer_id, message=event.payload,
        attachments=",".join(event.attachments))
    return "ok"
