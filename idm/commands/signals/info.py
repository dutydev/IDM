from ...objects import dp, MySignalEvent, SignalEvent
from ...utils import edit_message, new_message, delete_message
from datetime import datetime
from idm import __version__
from ..my_signals.auto_friends_add import afa_thread
from ..my_signals.online import online_thread
from threading import Thread
import time

@dp.signal_event_handle('инфо', 'инфа', '-i', 'info')
def sinfo(event: SignalEvent) -> str:

    def is_alive(th: Thread) -> bool:
        if th == None:return False
        if not th.is_alive():return False
        return True

    if event.msg['from_id'] not in event.db.trusted_users:
        message_id = new_message(event.api, event.chat.peer_id, message='Я тебе не доверяю 😑')
        time.sleep(3)
        delete_message(event.api, event.chat.peer_id, message_id)
        return "ok"

    owner = event.api('users.get', user_ids=event.db.owner_id)[0]


    message = f"""Информация о дежурном:
    IDM v{__version__}
    Владелец: [id{owner['id']}|{owner['first_name']} {owner['last_name']}]
    Чатов: {len(event.db.chats.keys())}

    Информация о чате:
    Я {'' if event.chat.installed else 'не'} дежурный в чате {'✅' if event.chat.installed else '❌'}
    Iris ID: {event.chat.iris_id}
    Имя: {event.chat.name}

    """.replace('    ', '')
    new_message(event.api, event.chat.peer_id, message=message)
    return "ok"