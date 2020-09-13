from idm.objects import dp, Event
from idm.api_utils import get_msg_id

@dp.event_register('banGetReason')
def ban_get_reason(event: Event) -> str:
    event.api.msg_op(1, event.chat.peer_id, event.obj['message'], 
        reply_to=get_msg_id(event.api, event.chat.peer_id, event.obj['local_id']))   
    return "ok"