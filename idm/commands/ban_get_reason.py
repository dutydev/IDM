from ..objects import dp, Event
from .. import utils

@dp.event_handle(dp.Methods.BAN_GET_REASON)
def ban_get_reason(event: Event) -> str:
    utils.new_message(event.api, event.chat.peer_id, message=event.obj['message'], 
        reply_to=utils.get_msg_id(event.api, event.chat.peer_id, event.obj['local_id']))   
    
    return "ok"