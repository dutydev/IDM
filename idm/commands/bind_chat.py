from ..objects import dp, Event, MySignalEvent, DB
from ..lpcommands.utils import msg_op, get_msg
from microvk import VkApi

@dp.event_handle('bindChat')
def bind_chat(event: Event) -> str:
    msg_op(1, event.chat.peer_id, event.responses['chat_bind'].format(
    имя = event.chat.name))
    return "ok"