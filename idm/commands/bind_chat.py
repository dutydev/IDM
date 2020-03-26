from ..objects import dp, Event
from ..utils import edit_message

@dp.event_handle(dp.Methods.BIND_CHAT)
def bind_chat(event: Event) -> str:
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message="✅ ЧАТЕК ПОДКЛЮЧЕН!")
    return "ok"