from ..objects import dp, Event
from ..utils import new_message

@dp.event_handle(dp.Methods.BIND_CHAT)
def bind_chat(event: Event) -> str:
    new_message(event.api, event.chat.peer_id, 
            message=f"✅ Беседа распознана.")
    return "ok"