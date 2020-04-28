from ...objects import dp, SignalEvent
from ...utils import new_message
from datetime import datetime

@dp.signal_event_handle('пинг', 'пиу', 'кинг', 'тик')
def ping(event: SignalEvent) -> str:

    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)

    #c_time_str = str(datetime.fromtimestamp(round(c_time)))
    #v_time_str = str(datetime.fromtimestamp(round(event.msg['date'])))

    r_type = 'ПОНГ' if event.command == "пинг" else "ПАУ" if event.command == "пиу" else "ТОК" if event.command == "тик" else "КОНГ"

    if delta > 15:r_type += "\nМОРОСИТ КОНКРЕТНО КТО-ТО!!!!!"
    elif delta > 10:r_type += "\nЭЭЭЭЭ КТО МОРОСИТ?!"
    elif delta > 5:r_type += "\nМоросит кто-то, что ли?"
    else:r_type += "\nЕжжи по каефу работает всё"

    message = f"""{r_type}

    Ответ через: {delta} с.
    """.replace('    ', '')
    new_message(event.api, event.chat.peer_id, message=message)
    return "ok"