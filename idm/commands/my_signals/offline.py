from ...objects import dp, MySignalEvent
from ...lpcommands.utils import set_online_privacy, msg_op


@dp.my_signal_event_register('+оффлайн')
def hide_online(event: MySignalEvent):
    if set_online_privacy(event.db):
        msg = '🍭 Онлайн скрыт'
    else:
        msg = '🐶 Произошла ошибка'
    msg_op(2, event.chat.peer_id, msg, event.msg['id'])
    return "ok"


@dp.my_signal_event_register('-оффлайн')
def reveal_online(event: MySignalEvent):
    if set_online_privacy(event.db, 'all'):
        msg = '🍒 Онлайн открыт для всех'
    else:
        msg = '🐶 Произошла ошибка'
    msg_op(2, event.chat.peer_id, msg, event.msg['id'])
    return "ok"
    