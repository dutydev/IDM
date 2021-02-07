import threading
import typing

from idm import __version__
from ...objects import dp, MySignalEvent, SignalEvent
from ...utils import edit_message


@dp.my_signal_event_handle('инфо', 'инфа', '-i', 'info')
def info(event: typing.Union[MySignalEvent, SignalEvent]) -> str:
    owner = event.api('users.get', user_ids=event.db.owner_id)[0]

    message = f"""Информация о дежурном:
    IDM v{__version__}
    Владелец: [id{owner['id']}|{owner['first_name']} {owner['last_name']}]
    Чатов: {len(event.db.chats.keys())}

    Автодобавление в друзья: {'да' if 'AFA Thread' in [th.getName() for th in threading.enumerate()] else 'нет'}
    Вечный онлайн: {'да' if 'Online Thread' in [th.getName() for th in threading.enumerate()] else 'нет'}

    Панель управления: https://{event.db.host}/

    Информация о чате:
    Я дежурный в чате: {'да' if event.chat.installed else 'нет'}
    Iris ID: {event.chat.iris_id}
    Peer ID: {event.chat.peer_id}
    Имя: {event.chat.name}
    
    """.replace('    ', '')

    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=message)
    return "ok"
