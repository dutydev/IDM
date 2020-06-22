from ...objects import dp, MySignalEvent, SignalEvent, __version__
from ...utils import edit_message, new_message
from datetime import datetime

@dp.my_signal_event_register('инфо', 'инфа', '-i', 'info')
def info(event: MySignalEvent) -> str:
    owner = event.api('users.get', user_ids=event.db.duty_id)[0]

    message = f"""Информация о дежурном:
    IDM-SC-mod v{__version__}
    Владелец: [id{owner['id']}|{owner['first_name']} {owner['last_name']}]
    Чатов: {len(event.db.chats.keys())}
    Шаблонов: {len(event.db.templates.keys())}

    Информация о чате:
    Я {'' if event.chat.installed else 'не'} дежурный в чате {'✅' if event.chat.installed else '❌'}
    Iris ID: {event.chat.iris_id}
    Имя: {event.chat.name}

    """.replace('    ', '')

    new_message(event.api, event.chat.peer_id,
    message=message, disable_mentions = 1)
    return "ok"