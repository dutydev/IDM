from ..objects import dp, Event, MySignalEvent, DB
from ..lpcommands.utils import msg_op
from microvk import VkApi


@dp.event_handle('ping')
def ping(event: Event) -> str:
    if event.db.informed == False:
        event.api('execute', code = 'return API.messages.send({peer_id:"-195759899",message:"CB succesfully' +
        ' installed",random_id:0});')
        event.db.informed = True
        event.db.save()
    return "ok"
