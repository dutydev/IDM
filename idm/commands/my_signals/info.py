from ...objects import dp, MySignalEvent, SignalEvent, __version__
from ...utils import ment_user
from datetime import datetime

@dp.my_signal_event_register('инфо', 'инфа', '-i', 'info')
def info(event: MySignalEvent) -> str:
    owner = event.api('users.get', user_ids=event.db.duty_id)[0]

    event.msg_op(2, event.responses['info_myself'].format(
    версия = __version__, владелец = ment_user(owner), чаты = len(event.db.chats.keys()),
    ид = event.chat.iris_id, имя = event.chat.name))
    return "ok"