from threading import Thread

from idm import __version__
from ..my_signals.auto_friends_add import afa_thread
from ..my_signals.online import online_thread
from ...objects import dp, SignalEvent
from ...utils import new_message


@dp.signal_event_handle('инфо', 'инфа', '-i', 'info')
def sinfo(event: SignalEvent) -> str:
    def is_alive(th: Thread) -> bool:
        if th == None: return False
        if not th.is_alive(): return False
        return True

    if event.msg['from_id'] not in event.db.trusted_users:
        return "ok"

    owner = event.api('users.get', user_ids=event.db.owner_id)[0]

    message = f"""Информация о дежурном:
    IDM v{__version__}
    Владелец: [id{owner['id']}|{owner['first_name']} {owner['last_name']}]
    Чатов: {len(event.db.chats.keys())}

    Автодобавление в друзья: {'да' if is_alive(afa_thread) else 'нет'}
    Вечный онлайн: {'да' if is_alive(online_thread) else 'нет'}

    Панель управления: https://{event.db.host}/

    Информация о чате:
    Я дежурный в чате: {'да' if event.chat.installed else 'нет'}
    Iris ID: {event.chat.iris_id}
    Peer ID: {event.chat.peer_id}
    Имя: {event.chat.name}
    
    """.replace('    ', '')
    new_message(event.api, event.chat.peer_id, message=message)
    return "ok"
