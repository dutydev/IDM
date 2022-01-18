from duty.objects import dp, MySignalEvent
from duty.api_utils import set_online_privacy


@dp.longpoll_event_register('+оффлайн')
@dp.my_signal_event_register('+оффлайн')
def hide_online(event: MySignalEvent):
    if set_online_privacy(event.db):
        msg = '🍭 Онлайн скрыт'
    else:
        msg = '🐶 Произошла ошибка'
    event.msg_op(2, msg)
    return "ok"


@dp.longpoll_event_register('-оффлайн')
@dp.my_signal_event_register('-оффлайн')
def reveal_online(event: MySignalEvent):
    if set_online_privacy(event.db, 'all'):
        msg = '🍒 Онлайн открыт для всех'
    else:
        msg = '🐶 Произошла ошибка'
    event.msg_op(2, msg)
    return "ok"
