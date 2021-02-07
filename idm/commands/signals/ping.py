from datetime import datetime

from ...objects import dp, SignalEvent
from ...utils import new_message


@dp.signal_event_handle('пинг', 'пиу', 'кинг')
def ping(event: SignalEvent) -> str:
    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)

    c_time_str = str(datetime.fromtimestamp(round(c_time)))
    v_time_str = str(datetime.fromtimestamp(round(event.msg['date'])))

    r_type = 'ПОНГ' if event.command == "пинг" else "ПАУ" if event.command == "пиу" else "КОНГ"

    if delta > 15:
        r_type += "\nТРЕВОГА. ШИНАПРОВОД СГРЫЗЕН!!!!"
    elif delta > 10:
        r_type += "\nТак кто-то конкретно грызет шинапровод."
    elif delta > 5:
        r_type += "\nТак кто-то начинает грызть шинапровод."
    else:
        r_type += "\neee сытый, спасибо, что накормили его."

    message = f"""{r_type}

    Ответ через: {delta}
    Время сервера VK:  {v_time_str}
    Время сервера IDM: {c_time_str}
    """.replace('    ', '')
    new_message(event.api, event.chat.peer_id, message=message)

    return "ok"
