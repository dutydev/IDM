from duty.objects import dp, Event
from duty.api_utils import get_msg_id


@dp.event_register('banGetReason')
def ban_get_reason(event: Event) -> str:
    reply = {}
    if event.obj['local_id'] != 0:
        reply['reply_to'] = get_msg_id(
            event.api, event.chat.peer_id, event.obj['local_id']
        )
    event.api.msg_op(1, event.chat.peer_id, event.obj['message'], **reply)
    return "ok"
