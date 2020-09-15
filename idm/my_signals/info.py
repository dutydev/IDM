from idm.objects import dp, MySignalEvent, SignalEvent, __version__
from idm.utils import ment_user
from .updating import get_last_version


@dp.longpoll_event_register('инфо', 'инфа', '-i', 'info')
@dp.my_signal_event_register('инфо', 'инфа', '-i', 'info')
def info(event: MySignalEvent) -> str:
    update_info = ''
    last_v, changes = get_last_version()
    if last_v != __version__:
        update_info = 'Доступно обновление! Новая версия: ' + last_v + '\n'
        if changes != '':
            update_info += 'Что нового:\n' + changes + '\n\n'
    owner = event.api('users.get', user_ids=event.db.duty_id)[0]
    message = event.responses['info_myself'].format(
        чаты=len(event.db.chats.keys()),
        владелец=ment_user(owner),
        ид=event.chat.iris_id,
        имя=event.chat.name,
        версия=__version__
    )
    event.msg_op(2, update_info + message)
    return "ok"
