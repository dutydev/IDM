from ...objects import dp, MySignalEvent, SignalEvent, __version__
from ...utils import edit_message, user_f
from datetime import datetime

@dp.my_signal_event_register('инфо', 'инфа', '-i', 'info')
def info(event: MySignalEvent) -> str:
    owner = event.api('users.get', user_ids=event.db.duty_id)[0]

    edit_message(event.api, event.chat.peer_id, event.msg['id'], message = event.responses['info_myself'].format(
    версия = __version__, владелец = user_f(owner), чаты = len(event.db.chats.keys()),
    ид = event.chat.iris_id, имя = event.chat.name))
    return "ok"