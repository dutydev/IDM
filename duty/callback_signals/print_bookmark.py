from duty.utils import cmid_key
from duty.objects import dp, Event
from duty.api_utils import get_msg_id


@dp.event_register('printBookmark')
def print_bookmark(event: Event) -> str:
    event.api.msg_op(1, event.chat.peer_id, event.obj['description'],
                     reply_to=get_msg_id(
                         event.api,
                         event.chat.peer_id,
                         event.obj[cmid_key]
                     ))
    return "ok"
