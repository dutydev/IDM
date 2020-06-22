from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
from datetime import datetime, date

@dp.my_signal_event_register('пинг', 'пиу', 'кинг', 'п', 'пингб', 'тик')
def ping(event: MySignalEvent) -> str:

    if event.command == 'пингб':
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message='PONG')
        return "ok"
    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)

    r_type = ('ПОНГ' if event.command == "пинг" else "ПАУ"
    if event.command == "пиу" else "ТОК" if event.command == "тик" else "КОНГ")

    edit_message(event.api, event.chat.peer_id, event.msg['id'],
    message = event.responses['ping_myself'].format(время = delta, ответ = r_type,
    обработано = round(datetime.now().timestamp() - event.time - event.vk_response_time, 2),
    пингвк = round(event.vk_response_time, 2)))
    return "ok"

