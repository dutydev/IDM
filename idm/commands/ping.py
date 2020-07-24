from ..objects import dp, Event, MySignalEvent, DB
from ..lpcommands.utils import msg_op
from microvk import VkApi


@dp.event_handle('ping')
def ping(event: Event) -> str:
    return "ok"
