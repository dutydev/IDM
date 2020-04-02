from ...objects import dp, MySignalEvent
from ...utils import new_message, edit_message

@dp.my_signal_event_handle('стик')
def stickers(event: MySignalEvent) -> str:

    if ((event.payload == '' or event.payload == None) and len(event.attachments) == 0) or len(event.args) == 0:
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Нет данных")
            return "ok"

    cat = " ".join(event.args)

    for temp in event.db.templates:
        if temp['name'] == name:

    new_message(event.api, event.chat.peer_id, message=f'cat = {cat}')
    return "ok"